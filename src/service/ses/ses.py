# -*- coding: utf-8 -*-
"""
This module has some functions to send an email using AWS SES.
"""

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import boto3
from src.layer.service.common.environment import isLocal, isDev, isSt, isDocker


# Charset on the email
CHARSET = "UTF-8"

# sender info
SENDER_EMAIL: str = os.environ.get("SES_SENDER_EMAIL", "sample@gmail.com")
SENDER_NAME: str = os.environ.get("SES_SENDER_NAME", "Sample, Inc.")

if isLocal():
    #  Local development config
    LOCAL_END_POINT_URL = os.environ.get(
        "SES_LOCAL_ENDPONIT_URL", "http://host.docker.internal:4579"
    )


""" send an email in HTML format.
Args:
    region_name (str): AWS region where the SES exists.
    recipients (list): recipient's email addresses.
    subject (str): the subject on the email.
    body (str): the body in HTML format on the email.
    attachments (list): the path of attachment files.
Returns:
    dict: the response from the SendRawEmail action.
"""


def sendHtmlMail(
    region_name: str, recipients: list, subject: str, body: str, attachments=None
) -> dict:
    return _sendMail(
        region_name=region_name,
        recipients=recipients,
        subject=subject,
        body_html=body,
        attachments=attachments,
    )


""" send an email in TEXT format.
Args:
    region_name (str): AWS region where the SES exists.
    recipients (list): recipient's email addresses.
    subject (str): the subject on the email.
    body (str): the body in TEXT format on the email.
    attachments (list): the path of attachment files.
Returns:
    dict: the response from the SendRawEmail action.
"""


def sendTextMail(
    region_name: str, recipients: list, subject: str, body: str, attachments=None
) -> dict:
    return _sendMail(
        region_name=region_name,
        recipients=recipients,
        subject=subject,
        body_text=body,
        ATTACHMENT=attachments,
    )


""" send an email.
Args:
    region_name (str): AWS region where the SES exists.
    recipients (list): recipient's email addresses.
    subject (str): the subject on the email.
    body_html (str): the body in HTML format on the email.
    body_text (str): the body in TEXT format on the email.
    attachments (list): the path of attachment files.
Returns:
    dict: the response from the SendRawEmail action.
"""


def _sendMail(
    region_name: str,
    recipients: list,
    subject: str,
    body_html: str = None,
    body_text: str = None,
    attachments: list = None,
) -> dict:
    # Create ses client.
    if isDocker():
        client = boto3.client(
            "ses",
            region_name=region_name,
            endpoint_url=LOCAL_END_POINT_URL,
        )
        client.verify_email_identity(EmailAddress=SENDER_EMAIL)
    else:
        client = boto3.client("ses", region_name=region_name)

    # Create sender info
    environment: str = ""
    if isLocal() is True:
        environment = "[local]"
    if isDev() is True:
        environment = "[develop]"
    if isSt() is True:
        environment = "[staging]"
    sender_name = Header(
        f"{environment}{SENDER_NAME}".encode("iso-2022-jp"), "iso-2022-jp"
    ).encode()
    sender: str = f"{sender_name} <{SENDER_EMAIL}>"

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart("mixed")
    # Add subject, from and to lines.
    msg["subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart("alternative")

    # Set html body.
    if body_html is not None:
        # The HTML body of the email.
        htmlpart = MIMEText(body_html.encode(CHARSET), "html", CHARSET)
        msg_body.attach(htmlpart)

    # Set text body.
    if body_text is not None:
        # The email body for recipients with non-HTML email clients.
        textpart = MIMEText(body_text.encode(CHARSET), "plain", CHARSET)
        msg_body.attach(textpart)

    # Attach files.
    if attachments is not None and len(attachments) != 0:
        for attachment in attachments:
            att = MIMEApplication(open(attachment, "rb").read())
            att.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(attachment),
            )
            msg.attach(att)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Send the email.
    # Provide the contents of the email.
    response = client.send_raw_email(
        Source=sender, Destinations=recipients, RawMessage={"Data": msg.as_string()}
    )
    return response
