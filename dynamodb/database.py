# -*- coding: utf-8 -*-

import boto3
import botocore
import os

# Botocore Config
# The maximum number of connections to keep in a connection pool.
# If this value is not set, the default value of 10 is used.
MAX_POOL_CONNECTIONS = os.environ.get("DYNAMODB_MAX_POOL_CONNECTIONS", 50)

"""
This class is an abstract class at AWS DynamoDB Table.
"""


class Database:
    def __init__(self, endpoint_url: str = None):
        # Initialize DynamoDB connection instance.
        if endpoint_url:
            self.client = boto3.client(
                "dynamodb",
                endpoint_url=endpoint_url,
                config=botocore.client.Config(
                    max_pool_connections=MAX_POOL_CONNECTIONS
                ),
            )
            self.resource = boto3.resource(
                "dynamodb",
                endpoint_url=endpoint_url,
                config=botocore.client.Config(
                    max_pool_connections=MAX_POOL_CONNECTIONS
                ),
            )
        else:
            self.client = boto3.client(
                "dynamodb",
                config=botocore.client.Config(
                    max_pool_connections=MAX_POOL_CONNECTIONS
                ),
            )
            self.resource = boto3.resource(
                "dynamodb",
                config=botocore.client.Config(
                    max_pool_connections=MAX_POOL_CONNECTIONS
                ),
            )

    def __del__(self):
        del self.resource
        del self.client

    # create a table.

    def createTable(self, json_data: dict) -> None:
        table_name = json_data["TableName"]
        if "ProvisionedThroughput" not in json_data:
            # On-demand mode
            billing_mode = "PAY_PER_REQUEST"
        else:
            # Provisioned mode
            billing_mode = "PROVISIONED"
            provisioned_throughput = json_data["ProvisionedThroughput"]

        # Create a table.
        if "LocalSecondaryIndexes" in json_data:
            if billing_mode == "PAY_PER_REQUEST":
                self.resource.create_table(
                    TableName=json_data["TableName"],
                    AttributeDefinitions=json_data["AttributeDefinitions"],
                    KeySchema=json_data["KeySchema"],
                    LocalSecondaryIndexes=json_data["LocalSecondaryIndexes"],
                    BillingMode=billing_mode,
                )
            else:
                self.resource.create_table(
                    TableName=json_data["TableName"],
                    AttributeDefinitions=json_data["AttributeDefinitions"],
                    KeySchema=json_data["KeySchema"],
                    LocalSecondaryIndexes=json_data["LocalSecondaryIndexes"],
                    BillingMode=billing_mode,
                    ProvisionedThroughput=provisioned_throughput,
                )
        else:
            if billing_mode == "PAY_PER_REQUEST":
                self.resource.create_table(
                    TableName=json_data["TableName"],
                    AttributeDefinitions=json_data["AttributeDefinitions"],
                    KeySchema=json_data["KeySchema"],
                    BillingMode=billing_mode,
                )
            else:
                self.resource.create_table(
                    TableName=json_data["TableName"],
                    AttributeDefinitions=json_data["AttributeDefinitions"],
                    KeySchema=json_data["KeySchema"],
                    BillingMode=billing_mode,
                    ProvisionedThroughput=provisioned_throughput,
                )

        # Wait until the table exists.
        self.client.get_waiter("table_exists").wait(TableName=table_name)

    # delete a table.

    def deleteTable(self, table_name: str) -> None:
        self.client.delete_table(TableName=table_name)
        self.client.get_waiter("table_not_exists").wait(TableName=table_name)

    def getTableList(self):
        return self.client.list_tables()["TableNames"]
