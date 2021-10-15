# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations
import os

from src.service.dynamodb.database import Database
import unittest

TEST_TABLE_NAME = "UtDatabaseTable"


class UtDynamodbDatabase(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        self.database = Database()

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        pass

    # the action before each of tests is executed in unittest
    def setUp(self):
        pass

    # the action after each of tests is executed in unittest
    def tearDown(self):
        pass

    def test_database_create(self):
        print(os.environ.get("AWS_LAMBDA_ENV"))
        ut_arg: dict = {
            "TableName": TEST_TABLE_NAME,
            "KeySchema": [
                {"AttributeName": "category", "KeyType": "HASH"},
                {"AttributeName": "id", "KeyType": "RANGE"},
            ],
            "AttributeDefinitions": [
                {"AttributeName": "category", "AttributeType": "S"},
                {"AttributeName": "id", "AttributeType": "N"},
                {"AttributeName": "date", "AttributeType": "S"},
                {"AttributeName": "price", "AttributeType": "N"},
            ],
            "LocalSecondaryIndexes": [
                {
                    "IndexName": "category-date-index",
                    "KeySchema": [
                        {"AttributeName": "category", "KeyType": "HASH"},
                        {"AttributeName": "date", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "category-price-index",
                    "KeySchema": [
                        {"AttributeName": "category", "KeyType": "HASH"},
                        {"AttributeName": "price", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
            ],
            "BillingMode": "PAY_PER_REQUEST",
        }
        expected: str = ut_arg["TableName"]
        actual: dict = self.database.createTable(ut_arg)
        # type test
        self.assertIs(type(actual), dict)
        self.assertIs(type(actual["TableDescription"]), dict)
        self.assertIs(type(actual["TableDescription"]["TableName"]), str)
        # value test
        self.assertEqual(actual["TableDescription"]["TableName"], expected)

        # check the table exists
        expected2: list = [TEST_TABLE_NAME]
        actual2: dict = self.database.getTableList()
        # type test
        self.assertIs(type(actual2), list)
        # value test
        self.assertEqual(actual2, expected2)

    def test_database_delete(self):
        ut_arg: str = TEST_TABLE_NAME
        expected: str = TEST_TABLE_NAME
        actual: dict = self.database.deleteTable(ut_arg)
        # type test
        self.assertIs(type(actual), dict)
        self.assertIs(type(actual["TableDescription"]), dict)
        self.assertIs(type(actual["TableDescription"]["TableName"]), str)
        # value test
        self.assertEqual(actual["TableDescription"]["TableName"], expected)

        # check the table does't exist.
        expected2: list = []
        actual2: dict = self.database.getTableList()
        # type test
        self.assertIs(type(actual2), list)
        # value test
        self.assertEqual(actual2, expected2)
