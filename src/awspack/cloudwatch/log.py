# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

import boto3

client = boto3.client("logs")


"""
Args:
    days (int): The number of days to retain the log events in the specified log group.
        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, and 3653.
    logGroupName (str, optional): The name of the log group.
Ref:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_retention_policy
"""


def setRetentionDays(days: int, logGroupName: str = None) -> None:
    if logGroupName is None:
        loggroups = getAllLogGroups()
        for loggroup in loggroups:
            client.put_retention_policy(
                logGroupName=loggroup["logGroupName"], retentionInDays=days
            )
    else:
        client.put_retention_policy(logGroupName=logGroupName, retentionInDays=days)


""" get all cloudwatch log groups.
Args:
    next_token(str, optional): A token to resume pagination.
Ref:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_log_groups
"""


def getAllLogGroups(next_token: str = None) -> list[dict]:
    loggroups: list = list()
    if next_token:
        result = client.describe_log_groups(nextToken=next_token)
    else:
        result = client.describe_log_groups()
    loggroups.extend(result["logGroups"])
    if len(result["logGroups"]) > 0 and "nextToken" in result:
        loggroups.extend(getAllLogGroups(result["nextToken"]))
    return loggroups


def getLogGroups(
    log_group_name_prefix: str = None, next_token: str = None
) -> list[dict]:
    loggroups: list = list()
    kwargs: dict = dict()
    if log_group_name_prefix is not None:
        kwargs["logGroupNamePrefix"] = log_group_name_prefix
    if next_token is not None:
        kwargs["nextToken"] = next_token
    result = client.describe_log_groups(**kwargs)
    loggroups.extend(result["logGroups"])
    if len(result["logGroups"]) > 0 and "nextToken" in result:
        loggroups.extend(getLogGroups(**kwargs))
    return loggroups
