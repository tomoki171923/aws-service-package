# -*- coding: utf-8 -*-
"""
This module has some functions to send an email using AWS SNS.
"""

import boto3
from src.layer.service.common.environment import isPro, isDocker


""" send an email in TEXT format.
Args:
    region_name (str): AWS region where the SNS is.
    topic_arn (str): SNS topic arn
    subject (str): the subject on the email.
    message (str): the body in TEXT format on the email.
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
    message_attributes: dict = None,
) -> dict:
    if isDocker():
        client = boto3.client(
            "sns",
            region_name=region_name,
            endpoint_url="http://host.docker.internal:4579",
        )
    else:
        client = boto3.client("sns", region_name=region_name)
    if not isPro():
        subject = "【dev/st環境】" + subject
    if message_attributes is None:
        response = client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject,
            MessageStructure="string",
        )
    else:
        response = client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject,
            MessageStructure="string",
            MessageAttributes=message_attributes,
        )
    return response
