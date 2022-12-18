# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

import boto3
import os
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

    """ getiing the list objects on the s3 bucket.
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
        return client.list_objects_v2(Bucket=bucket_name, Prefix=path)["Contents"]
