# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

import boto3

s3_resource = boto3.resource("s3")


class Bucket:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.bucket = s3_resource.Bucket(bucket_name)
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
        obj = s3_resource.Object(self.bucket_name, key=path)
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

    def ls(self, path: str):
        if self.client is None:
            self.client = boto3.client("s3")
        return self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=path)[
            "Contents"
        ]

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
        obj = s3_resource.Object(self.bucket_name, key=path)
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
        obj = s3_resource.Object(self.bucket_name, key=path)
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
        return s3_resource.Object(self.bucket_name, key=s3_path).download_file(
            local_path
        )

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
