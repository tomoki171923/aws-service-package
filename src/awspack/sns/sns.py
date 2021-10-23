# -*- coding: utf-8 -*-
"""
This module has some functions to send an email using AWS SNS.
"""

import boto3
from ..lambdalib.environment import isDev, isSt, isLocal


""" send an email in TEXT format.
Args:
    region_name (str): AWS region where the SNS exists.
    topic_arn (str): SNS topic arn
    subject (str): the subject on the email.
    message (str): the body in TEXT format on the email.
    message_structure (str, optional): Set MessageStructure to json if you want to send a different message for each protocol.
    message_attributes (dict, optional): The user-specified message attribute value.
        For string data types, the value attribute has the same restrictions on the content as the message body.
Returns:
    dict: the response from the SendEmail action.
"""


def sendMessage(
    region_name: str,
    topic_arn: str,
    subject: str,
    message: str,
    message_structure: str = None,
    message_attributes: dict = None,
) -> dict:
    client = boto3.client("sns", region_name=region_name)
    if isDev():
        subject = "[dev] " + subject
    if isSt():
        subject = "[staging] " + subject
    if isLocal():
        subject = "[local] " + subject
    kwargs: dict = {
        "TopicArn": topic_arn,
        "Message": message,
        "Subject": subject,
    }
    if message_structure is not None:
        kwargs["MessageStructure"] = message_structure
    if message_attributes is not None:
        kwargs["MessageAttributes"] = message_attributes
    response = client.publish(**kwargs)
    return response
