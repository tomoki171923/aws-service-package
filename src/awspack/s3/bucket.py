# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

import boto3
import os
from ..lambdalib.environment import isLocal, isDocker

resource_kargs: dict = dict()
if isDocker():
    resource_kargs["endpoint_url"] = os.environ.get(
        "S3_ENDPONIT_URL", "http://host.docker.internal:9000"
    )
elif isLocal():
    resource_kargs["endpoint_url"] = os.environ.get(
        "S3_ENDPONIT_URL", "http://localhost:9000"
    )
resource = boto3.resource("s3", **resource_kargs)


class Bucket:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.bucket = resource.Bucket(bucket_name)
        self.client = None

    """ getiing an object information on the s3 bucket.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.get
    Args:
        path (str):the object path.
    Returns:
        dict: the s3 object information.
    e.g.
        path = 'about/index.html'
            # => {'ResponseMetadata': {'RequestId': 'ZCCKH7NPZJZBYXXT', 'HostId':...
    """

    def get(self, path: str) -> dict:
        obj = resource.Object(self.bucket_name, key=path)
        return obj.get()

    """ getiing an object contents on the s3 bucket.
    Args:
        path (str):the object path.
    Returns:
        str: an object contents.
    e.g.
        path = 'about/index.html'
            # => '<!doctype html><html data-n-head-ssr lang="en" data-n-head="%7B%22lang%22:%7B%22ssr%22:%22en%22%7D%7D">...
    """

    def getContents(self, path: str) -> str:
        return self.get(path)["Body"].read().decode("utf-8")

    """ creating file on s3 bucket.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.put
    Args:
        acl (str):
            'private'|'public-read'|'public-read-write'|'authenticated-read'|'aws-exec-read'|'bucket-owner-read'|'bucket-owner-full-control'
        body (bytes | str): b'bytes'|file,
        path (str): the object path.
    Returns:
        dict: response object
    """

    def create(self, acl: str, body: bytes | str, path: str) -> dict:
        obj = resource.Object(self.bucket_name, key=path)
        response = obj.put(ACL=acl, Body=body)
        return response

    """ deleting file on s3 bucket.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.delete
    Args:
        path (str): the object path.
    Returns:
       dict: response object
    """

    def delete(self, path: str) -> dict:
        obj = resource.Object(self.bucket_name, key=path)
        response = obj.delete()
        return response

    """ downloading files from s3 bucket to local.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.upload_file
    Args:
        local_path (str): destination path to download object on local.
        s3_path (str): object path on s3 bucket.
    Returns:
        None
    e.g.
        local_path = '/tmp/hello.txt'
        s3_path = 'hello.txt'
    """

    def download(self, local_path: str, s3_path: str) -> None:
        return resource.Object(self.bucket_name, key=s3_path).download_file(local_path)

    """ uploading files from local to  s3 bucket.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.upload_file
    Args:
        local_path (str): file path on the local
        s3_path (str): destination path to place the object.
    Returns:
        None
    e.g.
        local_path = '/tmp/hello.txt'
        s3_path = 'hello.txt'
    """

    def upload(self, local_path: str, s3_path: str) -> None:
        return self.bucket.upload_file(local_path, s3_path)
