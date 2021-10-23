# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

# import os
import datetime
from decimal import Decimal
from src.awspack.dynamodb.table import Table

# from src.awspack.dynamodb.database import Database
from boto3.dynamodb.conditions import Attr
from pyutil.datetime_jp import today, pastDate, futureDate
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


def testdata60() -> list:
    utitems: list = list()
    thisdate = datetime.date(2021, 1, 1)
    for i in range(60):
        category: str
        name: str
        price = 100
        if i < 10:
            category = "Food"
            name = f"{category}{i}"
            price = 1000 + i * 10
            date = futureDate(thisdate, i)
        elif 10 <= i < 20:
            category = "Book"
            name = f"{category}{i}"
            price = 1000 + i * 100
            date = futureDate(thisdate, i)
        elif 20 <= i < 30:
            category = "Tablet"
            name = f"{category}{i}"
            price = 10000 + i * 1000
            date = pastDate(thisdate, i)
        else:
            category = "PC"
            name = f"{category}{i}"
            price = 200000 + i * 1000
            date = pastDate(thisdate, i)
        item: dict = {
            "category": category,
            "name": name,
            "id": 1000 + i,
            "price": price,
            "date": date.isoformat(),
        }
        utitems.append(item)
    return utitems


def testdata30() -> list:
    utitems: list = list()
    thisdate = today()
    for i in range(30):
        category: str
        name: str
        price = 100
        if i < 10:
            category = "Food"
            name = f"{category}{i}-new"
            price = 1000 + i * 10 + 200
            date = futureDate(thisdate, i)
        elif 10 <= i < 20:
            category = "Book"
            name = f"{category}{i}-new"
            price = 1000 + i * 100 + 200
            date = futureDate(thisdate, i)
        else:
            category = "Tablet"
            name = f"{category}{i}-new"
            price = 10000 + i * 1000 + 200
            date = pastDate(thisdate, i)
        item: dict = {
            "category": category,
            "name": name,
            "id": 1000 + i,
            "price": price,
            "date": date.isoformat(),
        }
        utitems.append(item)
    return utitems


class UtDynamodb(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        # self.database = Database()
        # self.database.createTable(TEST_TABLE)
        self.table = UtTable()
        self.table.update(testdata60())

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        self.table.delete(testdata60())
        self.table.delete(testdata30())
        # self.database.deleteTable(TEST_TABLE_NAME)

    # the action before each of tests is executed in unittest
    def setUp(self):
        pass

    # the action after each of tests is executed in unittest
    def tearDown(self):
        pass

    def test_1_find(self):
        ut_arg: str = "Food"
        ut_arg2: int = 1001
        expected: dict = {
            "name": "Food1",
            "date": "2021-01-02",
            "id": Decimal("1001"),
            "category": "Food",
            "price": Decimal("1010"),
        }
        actual = self.table.find(ut_arg, ut_arg2)
        # type test
        self.assertIs(type(actual), dict)
        # value test
        self.assertEqual(actual, expected)

    def test_1_where_1(self):
        ut_arg: str = "Food"
        ut_arg2: str = "2021-01-01"
        expected: int = 1
        expected2: list = [
            {
                "name": "Food0",
                "date": "2021-01-01",
                "id": Decimal("1000"),
                "category": "Food",
                "price": Decimal("1000"),
            }
        ]
        actual = self.table.where(category=ut_arg, date=ut_arg2)
        # type test
        self.assertIs(type(actual), list)
        self.assertIs(type(actual[0]), dict)
        # value test
        self.assertEqual(len(actual), expected)
        self.assertEqual(actual, expected2)

    def test_1_where_2(self):
        ut_arg: str = "Food"
        ut_arg2: str = "2021-01-01"
        ut_arg3: tuple = "#NAME, #DATE,  price"
        ut_arg4: dict = {
            "#DATE": "date",
            "#NAME": "name",
        }
        expected: int = 1
        expected2: list = [
            {"name": "Food0", "date": "2021-01-01", "price": Decimal("1000")}
        ]
        actual = self.table.where(
            category=ut_arg, date=ut_arg2, p_exp=ut_arg3, exp_attr_names=ut_arg4
        )
        # type test
        self.assertIs(type(actual), list)
        self.assertIs(type(actual[0]), dict)
        # value test
        self.assertEqual(len(actual), expected)
        self.assertEqual(actual, expected2)

    def test_1_where_3(self):
        ut_arg: str = "PC"
        expected: int = 30
        expected2: list = [td for td in testdata60() if td["category"] == "PC"]
        actual = self.table.where(category=ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.assertIs(type(actual[0]), dict)
        # value test
        self.assertEqual(len(actual), expected)
        self.assertEqual(actual, expected2)

    def test_2_put_1(self):
        ut_arg: dict = {
            "name": "Book111",
            "date": "2021-11-11",
            "id": Decimal("1111"),
            "category": "Book",
            "price": Decimal("1000"),
        }
        expected: dict = ut_arg
        actual = self.table.put(data=ut_arg)
        self.assertEqual(actual, None)
        actual2 = self.table.find(pk=ut_arg["category"], sk=ut_arg["id"])
        # type test
        self.assertIs(type(actual2), dict)
        # value test
        self.assertEqual(actual2, expected)

    def test_2_put_2(self):
        ut_arg: list = [
            {
                "name": "Book222",
                "date": "2021-11-12",
                "id": Decimal("2222"),
                "category": "Book",
                "price": Decimal("2000"),
            },
            {
                "name": "Book333",
                "date": "2021-11-12",
                "id": Decimal("3333"),
                "category": "Book",
                "price": Decimal("3000"),
            },
        ]
        expected: int = 2
        expected2: list = ut_arg
        actual = self.table.put(data=ut_arg)
        self.assertEqual(actual, None)
        actual2 = self.table.where(category="Book", date="2021-11-12")
        # type test
        self.assertIs(type(actual2), list)
        self.assertIs(type(actual2[0]), dict)
        # value test
        self.assertEqual(len(actual2), expected)
        self.assertEqual(actual2, expected2)

    def test_3_delete_1(self):
        ut_arg: dict = {
            "name": "Book111",
            "date": "2021-11-11",
            "id": Decimal("1111"),
            "category": "Book",
            "price": Decimal("1000"),
        }
        expected = None
        actual = self.table.delete(data=ut_arg)
        self.assertEqual(actual, None)
        actual2 = self.table.find(pk=ut_arg["category"], sk=ut_arg["id"])
        # value test
        self.assertEqual(actual2, expected)

    def test_3_delete_2(self):
        ut_arg: list = [
            {
                "name": "Book222",
                "date": "2021-11-12",
                "id": Decimal("2222"),
                "category": "Book",
                "price": Decimal("2000"),
            },
            {
                "name": "Book333",
                "date": "2021-11-12",
                "id": Decimal("3333"),
                "category": "Book",
                "price": Decimal("3000"),
            },
        ]
        expected: int = 0
        expected2: list = []
        actual = self.table.delete(data=ut_arg)
        self.assertEqual(actual, None)
        actual2 = self.table.where(category="Book", date="2021-11-12")
        # type test
        self.assertIs(type(actual2), list)
        # value test
        self.assertEqual(len(actual2), expected)
        self.assertEqual(actual2, expected2)

    def test_4_update_1(self):
        ut_arg: dict = {
            "name": "Food1-new",
            "date": "2021-10-10",
            "id": Decimal("1001"),
            "category": "Food",
            "price": Decimal("800"),
        }
        expected: dict = ut_arg
        actual = self.table.update(ut_arg)
        self.assertEqual(actual, None)
        actual2 = self.table.find(pk=ut_arg["category"], sk=ut_arg["id"])
        # type test
        self.assertIs(type(actual2), dict)
        # value test
        self.assertEqual(actual2, expected)

    def test_4_update_2(self):
        ut_arg: list = testdata30()
        expected: int = 10
        expected2: list = [td for td in testdata30() if td["category"] == "Food"]
        expected3: list = [td for td in testdata30() if td["category"] == "Book"]
        expected4: list = [td for td in testdata30() if td["category"] == "Tablet"]
        actual = self.table.update(data=ut_arg)
        self.assertEqual(actual, None)
        actual2 = self.table.where(category="Food")
        actual3 = self.table.where(category="Book")
        actual4 = self.table.where(category="Tablet")
        # type test
        self.assertIs(type(actual2), list)
        self.assertIs(type(actual3), list)
        self.assertIs(type(actual4), list)
        # value test
        self.assertEqual(len(actual2), expected)
        self.assertEqual(actual2, expected2)
        self.assertEqual(len(actual3), expected)
        self.assertEqual(actual3, expected3)
        self.assertEqual(len(actual4), expected)
        self.assertEqual(actual4, expected4)
