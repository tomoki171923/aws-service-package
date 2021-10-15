# -*- coding: utf-8 -*-

import boto3
import botocore
import os
from ..lambdalib.environment import isLocal, isDocker

# Botocore Config
# The maximum number of connections to keep in a connection pool.
# If this value is not set, the default value of 10 is used.
MAX_POOL_CONNECTIONS = os.environ.get("DYNAMODB_MAX_POOL_CONNECTIONS", 50)

# Initialize DynamoDB connection instance.
client_kargs: dict = {
    "config": botocore.client.Config(max_pool_connections=MAX_POOL_CONNECTIONS)
}
if isDocker():
    client_kargs["endpoint_url"] = os.environ.get(
        "DYNAMODB_ENDPONIT_URL", "http://host.docker.internal:8000"
    )
elif isLocal():
    client_kargs["endpoint_url"] = os.environ.get(
        "DYNAMODB_ENDPONIT_URL", "http://localhost:8000"
    )
client = boto3.client("dynamodb", **client_kargs)

"""
This class is an abstract class at AWS DynamoDB Table.
"""


class Database:
    def __init__(self) -> None:
        pass

    def __del__(self) -> None:
        pass

    # create a table.
    # ref https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
    def createTable(self, kwargs: dict) -> dict:
        table_name = kwargs["TableName"]
        res = client.create_table(**kwargs)
        # Wait until the table is created.
        client.get_waiter("table_exists").wait(TableName=table_name)
        return res

    # delete a table.
    def deleteTable(self, table_name: str) -> dict:
        res = client.delete_table(TableName=table_name)
        # Wait until the table is destroyed.
        client.get_waiter("table_not_exists").wait(TableName=table_name)
        return res

    def getTableList(self) -> list:
        return client.list_tables()["TableNames"]
