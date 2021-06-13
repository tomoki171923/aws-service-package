# -*- coding: utf-8 -*-

import json
import os
import boto3
import botocore


''' Executing another lambda function synchronously
Args:
    function_region (str): the region of function.
    function_name (list): another lambda function name.
    event (dict): the event data of argument.
Returns:
    dict: The response from the function, or an error object.
'''


def invokeLambdaSync(function_region: str, function_name: str, event: dict) -> dict:
    return __execLambda(function_region, function_name, event, 'RequestResponse')


''' Executing another lambda function asynchronously
Args:
    function_region (str): the region of function.
    function_name (list): another lambda function name.
    event (dict): the event data of argument.
Returns:
    dict: The response from the function, or an error object.
'''


def invokeLambdaAsync(function_region: str, function_name: str, event: dict) -> dict:
    return __execLambda(function_region, function_name, event, 'Event')


''' Executing another lambda function
Ref : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke
Args:
    function_region (str): the region of function.
    function_name (list): another lambda function name.
    event (dict): the event data of argument.
    invocationType (str): RequestResponse or Event or DryRun.
Returns:
    dict: The response from the function, or an error object.
'''


def __execLambda(function_region: str, function_name: str, event: dict, invocationType: str) -> dict:
    lambda_client = boto3.client('lambda', function_region)
    # when function version is $LATEST, doesn't specify alias
    # but in other case specify it
    if os.environ['AWS_LAMBDA_FUNCTION_VERSION'] == '$LATEST':
        function = function_name
    else:
        function = f"{function_name}:{os.environ['AWS_LAMBDA_FUNCTION_ALIAS']}"

    response: botocore.response.StreamingBody = lambda_client.invoke(
        FunctionName=function,
        InvocationType=invocationType,
        Payload=json.dumps(event)
    )
    payLoad: bytes = response['Payload'].read()
    return json.loads(payLoad.decode('utf-8'))
