# -*- coding: utf-8 -*-
'''
This module has some functions to send an email using AWS SES.
'''

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import boto3
from src.layer.logic import myconst
from src.layer.service.common.environment import isDev, isSt


# Charset on the email
CHARSET = "UTF-8"

# Create a client & set the sender.
# Reference: address the corrupted text
# https://qiita.com/danishi/items/769409ebfcd26365ec9e
environment = ''
if 'DOCKER_LAMBDA_DEBUG' in os.environ:
    # CASE: Local environment
    environment = '【ローカル】'
    SENDER_NAME = Header(f"{environment}{myconst.cst.SENDER_NAME}".encode(
        'iso-2022-jp'), 'iso-2022-jp').encode()
    CLIENT = boto3.client('ses', region_name=myconst.cst.REGION,
                          endpoint_url='http://host.docker.internal:4579')
    CLIENT.verify_email_identity(EmailAddress=myconst.cst.SENDER_EMAIL)
else:
    # CASE: AWS environment
    if isDev():
        # development environment on AWS
        environment = '【開発】'
    elif isSt():
        # staging environment on AWS
        environment = '【テスト】'
    SENDER_NAME = Header(f"{environment}{myconst.cst.SENDER_NAME}".encode(
        'iso-2022-jp'), 'iso-2022-jp').encode()
    CLIENT = boto3.client('ses', region_name=myconst.cst.REGION)
SENDER = f'{SENDER_NAME} <{myconst.cst.SENDER_EMAIL}>'


''' send an email in HTML format.
Args:
    recipients (list): recipient's email addresses.
    subject (str): the subject on the email.
    body (str): the body in HTML format on the email.
    attachments (list): the path of attachment files.
Returns:
    dict: the response from the SendRawEmail action.
'''


def sendHtmlMail(recipients: list, subject: str, body: str, attachments=None):
    return _sendMail(RECIPIENTS=recipients, SUBJECT=subject, BODY_HTML=body, ATTACHMENTS=attachments)


''' send an email in TEXT format.
Args:
    recipients (list): recipient's email addresses.
    subject (str): the subject on the email.
    body (str): the body in TEXT format on the email.
    attachments (list): the path of attachment files.
Returns:
    dict: the response from the SendRawEmail action.
'''


def sendTextMail(recipients: list, subject: str, body: str, attachments=None)):
    return _sendMail(RECIPIENTS = recipients, SUBJECT = subject, BODY_TEXT = body, ATTACHMENT = attachments)


''' send an email.
Args:
    RECIPIENTS (list): recipient's email addresses.
    SUBJECT (str): the subject on the email.
    BODY_HTML (str): the body in HTML format on the email.
    BODY_TEXT (str): the body in TEXT format on the email.
    ATTACHMENTS (list): the path of attachment files.
Returns:
    dict: the response from the SendRawEmail action.
'''
def _sendMail(RECIPIENTS, SUBJECT, BODY_HTML = None, BODY_TEXT = None, ATTACHMENTS = None):
    # Create a multipart/mixed parent container.
    msg=MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject']=SUBJECT
    msg['From']=SENDER
    msg['To']=', '.join(RECIPIENTS)

    # Create a multipart/alternative child container.
    msg_body=MIMEMultipart('alternative')

    # Set html body.
    if BODY_HTML is not None:
        # The HTML body of the email.
        htmlpart=MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        msg_body.attach(htmlpart)

    # Set text body.
    if BODY_TEXT is not None:
        # The email body for recipients with non-HTML email clients.
        textpart=MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
        msg_body.attach(textpart)

    # Attach files.
    if ATTACHMENTS is not None and len(ATTACHMENTS) != 0:
        for attachment in ATTACHMENTS:
            att=MIMEApplication(open(attachment, 'rb').read())
            att.add_header('Content-Disposition', 'attachment',
                           filename = os.path.basename(attachment))
            msg.attach(att)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Send the email.
    # Provide the contents of the email.
    response=CLIENT.send_raw_email(
        Source=SENDER,
        Destinations=RECIPIENTS,
        RawMessage={
            'Data': msg.as_string(),
        }
    )
    return response

