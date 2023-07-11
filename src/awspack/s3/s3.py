# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

import boto3
import os
import json
from ..lambdalib.environment import isLocal, isDocker


client_kargs: dict = dict()
if isDocker():
    client_kargs["endpoint_url"] = os.environ.get(
        "S3_ENDPONIT_URL", "http://host.docker.internal:9000"
    )
elif isLocal():
    client_kargs["endpoint_url"] = os.environ.get(
        "S3_ENDPONIT_URL", "http://localhost:9000"
    )

client = boto3.client("s3", **client_kargs)


class S3:
    def __init__(self) -> None:
        pass

    def __del__(self) -> None:
        pass

    # create a table.
    # ref https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket
    def createBucket(self, kwargs: dict) -> dict:
        res = client.create_bucket(**kwargs)
        return res

    # delete a table.
    # ref https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket
    def deleteBucket(self, kwargs: dict) -> dict:
        res = client.delete_bucket(**kwargs)
        return res

    """ getting the list objects on the s3 bucket.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
    Args:
        path (str): objects root path.
    Returns:
        list: objects contents.
    e.g.
        path = 'about/'
            # => [{'Key': 'about/index.html',
                    'LastModified': datetime.datetime(2021, 7, 2, 16, 36, 54, tzinfo=tzlocal()),
                    'ETag': '"b2b1a0db93f5a4598685763fd7b72823"', 'Size': 364050, 'StorageClass': 'STANDARD'},...
                ]
    """

    def ls(self, bucket_name: str, path: str) -> list:
        res: dict = client.list_objects_v2(Bucket=bucket_name, Prefix=path)
        if "Contents" in res:
            return res["Contents"]
        else:
            return []

    """ select the objects on the s3 bucket with the S3 SQL expression.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content
    https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-glacier-select-sql-reference-select.html
    Args:
        kwargs (dict): s3 select arguments.
        format (bool, optional): wethere format.
    Returns:
        dict | list: the result of a s3 select query.
    """

    def select(self, kwargs: dict, format: bool = True) -> dict | list:
        if format is False:
            return client.select_object_content(**kwargs)
        kwargs["OutputSerialization"] = {
            "JSON": {
                "RecordDelimiter": "\n",
            }
        }
        res: dict = client.select_object_content(**kwargs)
        if "JSON" in kwargs["InputSerialization"]:
            if kwargs["InputSerialization"]["JSON"]["Type"] == "LINES":
                return self.__formatSelectQuery(res, "JSONL")
            else:
                return self.__formatSelectQuery(res, "JSON")
        if "CSV" in kwargs["InputSerialization"]:
            return self.__formatSelectQuery(res, "CSV")

    def __formatSelectQuery(self, res: dict, format_type: str) -> dict | list:
        if format_type == "JSON":
            for event in res["Payload"]:
                if "Records" in event:
                    return json.loads(event["Records"]["Payload"].decode("UTF-8"))
        elif format_type == "JSONL":
            result: list = []
            text: str = ""
            for event in res["Payload"]:
                if "Records" in event:
                    raw = event["Records"]["Payload"].decode("UTF-8")
                    text += raw
            for line in text.splitlines():
                result.append(json.loads(line))
        elif format_type == "CSV":
            result: list = []
            text: str = ""
            for event in res["Payload"]:
                if "Records" in event:
                    raw = event["Records"]["Payload"].decode("UTF-8")
                    text += raw
            for line in text.splitlines():
                result.append(json.loads(line))
        return result
