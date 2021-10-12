# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations
import os

os.environ["AWS_LAMBDA_ENV"] = "local"

from src.service.dynamodb.table import Table
from src.service.dynamodb.database import Database
from boto3.dynamodb.conditions import Attr
import unittest

TEST_TABLE_NAME = "UtTable"
TEST_TABLE = {
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


class UtTable(Table):
    def __init__(self):
        super().__init__(TEST_TABLE_NAME, pk_name="category", sk_name="id")

    def __del__(self):
        super().__del__()

    def where(
        self,
        category: str,
        date: str = None,
        p_exp: str = None,
        exp_attr_names: dict = None,
    ) -> list:
        f_exp = None
        if date is not None:
            f_exp = (
                Attr("date").eq(date)
                if f_exp is None
                else f_exp & Attr("#ate").eq(date)
            )
        result = self._queryTable(
            pk=category, p_exp=p_exp, f_exp=f_exp, exp_attr_names=exp_attr_names
        )
        return result

    def update(self, data: list | dict) -> None:
        self.delete(data)
        self.put(data)


class UtDynamodb(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        self.database = Database()
        self.database.createTable(TEST_TABLE)

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        pass
        # self.database.deleteTable(TEST_TABLE_NAME)

    # the action before each of tests is executed in unittest
    def setUp(self):
        pass

    # the action after each of tests is executed in unittest
    def tearDown(self):
        pass

    def test_put_1(self):
        pass

    def test_put_2(self):
        pass

    def test_delete_1(self):
        pass

    def test_delete_2(self):
        pass

    def test_update_1(self):
        pass

    def test_update_2(self):
        pass

    def test_find(self):
        pass

    def test_where_1(self):
        pass

    def test_where_2(self):
        pass

    def test_where_3(self):
        pass
