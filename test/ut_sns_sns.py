import unittest
import os

from src.awspack.sns.sns import (
    sendMessage,
)


class UtCloudwatchLog(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        pass

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        pass

    def test_sendMessage(self):
        ut_arg: str = "ap-northeast-1"
        ut_arg2: str = os.environ.get("SNS_TOPIC_ARN")
        ut_arg3: str = "unittest"
        ut_arg4: str = "this is an unittest."
        expected: int = 200
        actual = sendMessage(
            region_name=ut_arg,
            topic_arn=ut_arg2,
            subject=ut_arg3,
            message=ut_arg4,
        )
        # type test
        self.__sns_type_test(actual)
        # value test
        self.assertEqual(actual["ResponseMetadata"]["HTTPStatusCode"], expected)

    def __sns_type_test(self, sns_res: dict):
        self.assertIs(type(sns_res), dict)
        self.assertIs(type(sns_res["MessageId"]), str)
        self.assertIs(type(sns_res["ResponseMetadata"]), dict)
        self.assertIs(type(sns_res["ResponseMetadata"]["RequestId"]), str)
        self.assertIs(type(sns_res["ResponseMetadata"]["HTTPStatusCode"]), int)
        self.assertIs(type(sns_res["ResponseMetadata"]["RetryAttempts"]), int)
        self.assertIs(type(sns_res["ResponseMetadata"]["HTTPHeaders"]), dict)
        self.assertIs(
            type(sns_res["ResponseMetadata"]["HTTPHeaders"]["x-amzn-requestid"]), str
        )
        self.assertIs(
            type(sns_res["ResponseMetadata"]["HTTPHeaders"]["content-type"]), str
        )
        self.assertIs(
            type(sns_res["ResponseMetadata"]["HTTPHeaders"]["content-length"]), str
        )
        self.assertIs(type(sns_res["ResponseMetadata"]["HTTPHeaders"]["date"]), str)
