# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

import boto3

client = boto3.client('logs')


'''
Args:
    days (int): The number of days to retain the log events in the specified log group.
        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, and 3653.
'''
def setRetentionDays(days:int) -> None:
    loggroups = getAllLogGroups()
    for loggroup in loggroups:
        client.put_retention_policy(logGroupName=loggroup['logGroupName']
                                    , retentionInDays=days)


''' get all cloudwatch log groups.
Args:
    next_token(str, optional): A token to resume pagination.
Ref:
    loggroup sample.
        {
            'logGroupName': '/aws/lambda/helloWorld', 
            'creationTime': 1614166944408, 
            'metricFilterCount': 0, 
            'arn': 'arn:aws:logs:ap-northeast-1:1234567890:log-group:/aws/lambda/helloWorld:*', 
            'storedBytes': 0
        }
'''         
def getAllLogGroups(next_token:str=None) -> dict:
    loggroups :list = list()
    if next_token:
        result = client.describe_log_groups(nextToken=next_token)
    else:
        result = client.describe_log_groups()
    loggroups.extend(result['logGroups'])
    if len(result['logGroups']) > 0 and 'nextToken' in result:
        loggroups.extend(getAllLogGroups(result['nextToken']))
    return loggroups


