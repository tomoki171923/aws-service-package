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
        p_exp (str, optional): ProjectionExpression of query paramers. e.g. 'country, area')
        f_exp (str, optional): FilterExpression of query paramers.
    """

    def __init__(
        self,
        query: Callable[[], dict],
        kc_exp: str,
        p_exp: str = None,
        f_exp: str = None,
    ):
        self.__query = query
        self.setter(kc_exp=kc_exp, p_exp=p_exp, f_exp=f_exp)

    # destructor.

    def __del__(self):
        del self.__kwargs
        del self.__result
        del self.__next_key
        del self.__query

    """ set query paramers.
    Args:
        kc_exp (str): KeyConditionExpression of query paramers.
        p_exp (str, optional): ProjectionExpression of query paramers. e.g. 'country, area')
        f_exp (str, optional): FilterExpression of query paramers.
    """

    def setter(self, kc_exp: str, p_exp: str = None, f_exp: str = None) -> None:
        self.__kwargs = {"KeyConditionExpression": kc_exp}
        if p_exp is not None:
            self.__kwargs["ProjectionExpression"] = p_exp
        if f_exp is not None:
            self.__kwargs["FilterExpression"] = f_exp
        self.__next_key = None
        self.__result = list()

    def __next(self):
        if self.__next_key is not None:
            self.__kwargs["ExclusiveStartKey"] = self.__next_key
        response = self.__query(**self.__kwargs)
        self.__result.extend(response["Items"])
        if "LastEvaluatedKey" in response:
            self.__next_key = response["LastEvaluatedKey"]
            self.__next()

    """ execute query method of DynamoDB Table class.
    Returns:
        list: the result of a Query operation.
    """

    def run(self) -> list:
        response = self.__query(**self.__kwargs)
        if "Items" not in response:
            return None
        self.__result.extend(response["Items"])
        if "LastEvaluatedKey" in response:
            self.__next_key = response["LastEvaluatedKey"]
            self.__next()
        self.__next_key = None
        return self.__result
