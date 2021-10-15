# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

from src.service.dynamodb.database import Database
from src.service.dynamodb.table import Table
from boto3.dynamodb.conditions import Attr

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


database = Database()
database.createTable(TEST_TABLE)


table = UtTable()


testdata: list = list()

for i in 30:
    print(i)
