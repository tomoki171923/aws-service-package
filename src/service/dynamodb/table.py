# -*- coding: utf-8 -*-
# the following is not necessary if Python version is 3.9 or over.
from __future__ import annotations

from abc import ABCMeta, abstractmethod
import boto3
import botocore
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import os
import inspect
from src.layer.util.split import splitList
from src.layer.util.time_watch import TimeWatch
from src.layer.service.common.environment import isPro, isLocal
from src.layer.service.dynamodb.query import Query


# Botocore Config
# The maximum number of connections to keep in a connection pool.
# If this value is not set, the default value of 10 is used.
MAX_POOL_CONNECTIONS = os.environ.get("DYNAMODB_MAX_POOL_CONNECTIONS", 50)

# Initialize DynamoDB connection instance.
if isLocal():
    #  Local development config
    LOCAL_END_POINT_URL = os.environ.get(
        "DYNAMODB_LOCAL_ENDPONIT_URL", "http://host.docker.internal:8000"
    )
    resource = boto3.resource(
        "dynamodb",
        endpoint_url=LOCAL_END_POINT_URL,
        config=botocore.client.Config(max_pool_connections=MAX_POOL_CONNECTIONS),
    )
else:
    resource = boto3.resource(
        "dynamodb",
        config=botocore.client.Config(max_pool_connections=MAX_POOL_CONNECTIONS),
    )

"""
This class is an abstract class at AWS DynamoDB Table.
"""


class Table(metaclass=ABCMeta):
    # this number is the maximum number of can comprise requests.
    ITEM_COUNT = 25

    """ abstract Method. the concrete class has to override this method.
        constructor.
    Args:
        table_name (str): table name.
        pk_name (str): partition key's name.
        sk_name (str, optional): sort key's name.
    """

    @abstractmethod
    def __init__(self, table_name: str, pk_name: str, sk_name: str = None):
        self.table: boto3.resource.table = resource.Table(table_name)
        self.table_name = table_name
        self.pk_name = pk_name
        self.sk_name = sk_name
        self.query = None
        self.total_rcu = 0.0
        self.total_read_content_size = 0
        self.total_wcu = 0.0
        self.split_list = splitList
        self.IS_PRO = isPro()
        if not self.IS_PRO:
            self.time_watch = TimeWatch()

    # destructor.

    def __del__(self):
        if not self.IS_PRO:
            del self.time_watch
        del self.split_list
        del self.total_wcu
        del self.total_read_content_size
        del self.total_rcu
        if self.query is not None:
            del self.query
        del self.sk_name
        del self.pk_name
        del self.table_name
        del self.table

    """ finding the item.
    Args:
        pk (str): partition key.
        sk (str): sort key.
    Returns:
        dict: the result of a Query operation.
    """

    def find(self, pk: str, sk: str) -> dict:
        response = self.table.get_item(Key={self.pk_name: pk, self.sk_name: sk})
        key = "Item"
        if key not in response:
            return None
        return self._filter(response, key)

    # abstract Method. the concrete class has to override this method.
    # finding items.

    @abstractmethod
    def where(self):
        pass

    # abstract Method. the concrete class has to override this method.
    # updating items.

    @abstractmethod
    def update(self):
        pass

    """ put an item or items into the table.
    Args:
        data (dict or list): an item or items putting into the table.
    """

    def put(self, data: list | dict) -> None:
        if not self.IS_PRO:
            # start measuring the run time.
            action_name = f"put items into the {self.table_name} table"
            self.time_watch.start(action_name)
        if type(data) is dict:
            # put an item
            self.table.put_item(Item=self.__formatItem(data))
        elif type(data) is list:
            # put items
            if len(data) == 0:
                return
            for batch_items in self.split_list(data, Table.ITEM_COUNT):
                request_items: list = list(map(self.__getBatchRequest, batch_items))
                self.__batchWriteItem(request_items)
        else:
            return
        if not self.IS_PRO:
            # stop measuring the run time & print log.
            self.time_watch.stop(action_name)

    """ delete an item or items on the table.
    Args:
        data (dict or list): an item or items deleting on the table.
    """

    def delete(self, data: list | dict) -> None:
        if not self.IS_PRO:
            # start measuring the run time.
            action_name = f"delete items on the {self.table_name} table"
            self.time_watch.start(action_name)
        if type(data) is dict:
            # delete an item
            formated_data = self.__formatItem(data)
            self.table.delete_item(Key=self.__getRequestKey(formated_data))
        elif type(data) is list:
            # delete items
            if len(data) == 0:
                return
            for batch_items in self.split_list(data, Table.ITEM_COUNT):
                request_items: list = list(map(self.__getBatchRequest, batch_items))
                self.__batchWriteItem(request_items)
        else:
            return
        if not self.IS_PRO:
            # stop measuring the run time & print log.
            self.time_watch.stop(action_name)

    # log total WCU, RCU and loaded contents size on the table.

    def reportPerformance(self) -> None:
        print("************ Performance Log ************")
        print(f"table: {self.table_name}")
        print(f"total_rcu: {self.total_rcu}")
        print(f"total_read_content_size: {self.total_read_content_size}")
        print(f"total_wcu: {self.total_wcu}")
        print("******************************************")

    """ filtering a response.
    Args:
        response (dict): a response from a DynamoDB operation.
        key (str): the key to filter.
    Returns:
        dict: the filtered response.
    """

    def _filter(self, response: dict, key: str) -> dict:
        return response[key]

    """ filtering a result data from a Query operation.
    Args:
        data (dict): the result data from a Query operation.
    Returns:
        dict: the filtered result.
    """

    def _filterQuery(self, data: dict) -> dict:
        del data["Count"]
        del data["ScannedCount"]
        del data["ResponseMetadata"]
        return data

    """ format an item which puts into the table.
        (convert Float into Decimal in the item)
    Args:
        item (dict): an unformatted item
    Returns:
        dict: a formatted item.
    """

    def __formatItem(self, item: dict) -> dict:
        formatted_item = dict()
        for k, v in item.items():
            if type(v) is dict:
                formatted_item[k] = self.__formatItem(v)
            elif type(v) is list:
                value_list = list()
                if type(v[0]) is str or type(v[0]) is int:
                    # [111, 222, 333] or ['aaa', 'bbb', 'ccc']
                    value_list = v
                else:
                    # [{},{},{}] or [[],[],[]]
                    for each_v in v:
                        value_list.append(self.__formatItem(each_v))
                formatted_item[k] = value_list
            elif type(v) is float:
                formatted_item[k] = Decimal(str(v))
            else:
                formatted_item[k] = v
        return formatted_item

    """ get a request key to read or delete an item from table.
    Args:
        item (dict): an item.
    Returns:
        dict: request key.
    """

    def __getRequestKey(self, item: dict) -> dict:
        request_key = dict()
        for attribute_name in self.table.key_schema:
            attr_name = attribute_name["AttributeName"]
            request_key[attr_name] = item[attr_name]
        return request_key

    """ get a request for batch_write_item method which DynamoDB.ServiceResource class has.
        DeleteRequest -
            Perform a DeleteItem operation on the specified item. The item to be deleted is identified by a Key subelement:
        PutRequest -
            Perform a PutItem operation on the specified item. The item to be put is identified by an Item subelement:
    Args:
        item (dict): an item.
    Returns:
        dict: request for batch_write_item method.
    """

    def __getBatchRequest(self, item: dict) -> dict:
        caller = inspect.stack()[1].function
        if caller == "put":
            return {"PutRequest": {"Item": self.__formatItem(item)}}
        elif caller == "delete":
            request = {"DeleteRequest": {"Key": {}}}
            for attribute_name in self.table.key_schema:
                name = attribute_name["AttributeName"]
                request["DeleteRequest"]["Key"][name] = item[name]
            return request

    """ execute batch_write_item method which DynamoDB.ServiceResource class has.
        The BatchWriteItem operation puts or deletes multiple items in one or more tables.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.batch_write_item
    Args:
        request_items (list): request items.
    """

    def __batchWriteItem(self, request_items: list) -> None:
        resutn_consumed_capacity: str = "INDEXES" if not self.IS_PRO else "NONE"
        response = resource.batch_write_item(
            RequestItems={self.table_name: request_items},
            ReturnConsumedCapacity=resutn_consumed_capacity,
        )
        if "ConsumedCapacity" in response:
            self.total_wcu += response["ConsumedCapacity"][0]["CapacityUnits"]
        if "UnprocessedItems" in response and response["UnprocessedItems"] != {}:
            unprocessed_items = response["UnprocessedItems"][self.table_name]
            if len(unprocessed_items) > 0:
                self.__batchWriteItem(unprocessed_items)

    """ override.
        query items to the table on DynamoDB.
    Args:
        pk (str): partition key.
        p_exp (str, optional): ProjectionExpression of query paramers. e.g. 'country, area')
        f_exp (str, optional): FilterExpression of query paramers.
        exp_attr_names (dict, optional): ExpressionAttributeNames of query paramers.
    Returns:
        list: the result of a Query operation.
    """

    def _queryTable(
        self,
        pk: str,
        p_exp: str = None,
        f_exp: str = None,
        exp_attr_names: dict = None,
    ) -> list:
        if not self.IS_PRO:
            # start measuring the run time.
            action_name = f"{self.table_name} query"
            self.time_watch.start(action_name)
        kc_exp = Key(self.pk_name).eq(pk)

        if self.query is None:
            # create Query instance
            self.query = Query(
                self.table.query,
                kc_exp=kc_exp,
                p_exp=p_exp,
                f_exp=f_exp,
                exp_attr_names=exp_attr_names,
            )
        else:
            # set params
            self.query.setter(
                kc_exp=kc_exp, p_exp=p_exp, f_exp=f_exp, exp_attr_names=exp_attr_names
            )

        response = self.query.run()
        if not self.IS_PRO:
            # stop measuring the run time & print log.
            self.time_watch.stop(action_name)
        return response
