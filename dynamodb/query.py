# -*- coding: utf-8 -*-

"""
This class is query operation class at AWS DynamoDB Table.
"""

from typing import Callable


class Query:
    """ constructor
    Ref:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.query
    Args:
        query (Callable[[], dict]): query method of DynamoDB Table class.
        kc_exp (str): KeyConditionExpression of query paramers.
        f_exp (str, optional): FilterExpression of query paramers.
    """

    def __init__(self, query: Callable[[], dict], kc_exp: str, f_exp: str = None):
        self.__query = query
        self.setter(kc_exp, f_exp)

    # destructor.

    def __del__(self):
        del self.__result
        del self.__next_key
        del self.__f_exp
        del self.__kc_exp
        del self.__query

    """ set query paramers.
    Args:
        kc_exp (str): KeyConditionExpression of query paramers.
        f_exp (str, optional): FilterExpression of query paramers.
    """

    def setter(self, kc_exp: str, f_exp: str = None) -> None:
        self.__kc_exp = kc_exp
        self.__f_exp = f_exp
        self.__next_key = None
        self.__result = list()

    def __next(self):
        if self.__f_exp:
            response = self.__query(
                KeyConditionExpression=self.__kc_exp,
                FilterExpression=self.__f_exp,
                ExclusiveStartKey=self.__next_key,
            )
        else:
            response = self.__query(
                KeyConditionExpression=self.__kc_exp, ExclusiveStartKey=self.__next_key
            )
        self.__result.extend(response["Items"])
        if "LastEvaluatedKey" in response:
            self.__next_key = response["LastEvaluatedKey"]
            self.__next()

    """ execute query method of DynamoDB Table class.
    Returns:
        list: the result of a Query operation.
    """

    def run(self) -> list:
        if self.__f_exp:
            response = self.__query(
                KeyConditionExpression=self.__kc_exp, FilterExpression=self.__f_exp
            )
        else:
            response = self.__query(KeyConditionExpression=self.__kc_exp)
        if "Items" not in response:
            return None
        self.__result.extend(response["Items"])
        if "LastEvaluatedKey" in response:
            self.__next_key = response["LastEvaluatedKey"]
            self.__next()
        self.__next_key = None
        return self.__result
