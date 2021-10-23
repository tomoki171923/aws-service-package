import unittest

from src.awspack.cloudwatch.log import (
    setRetentionDays,
    getLogGroups,
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

    def test_getLogGroups(self):
        actual: list = getLogGroups()
        # type test
        self.assertIs(type(actual), list)
        self.__loggroup_type_test(actual[0])

    def test_getLogGroups2(self):
        ut_arg: str = "/aws/apigateway/welcome"
        actual: list = getLogGroups(log_group_name_prefix=ut_arg)
        expected: int = ut_arg
        # type test
        self.assertIs(type(actual), list)
        self.__loggroup_type_test(actual[0])
        # value test
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0]["logGroupName"], expected)

    def test_setRetentionDays(self):
        ut_arg: int = 60
        ut_arg2: str = "/aws/apigateway/welcome"
        expected: int = ut_arg
        expected2: int = ut_arg2
        setRetentionDays(days=ut_arg, logGroupName=ut_arg2)
        actual: list = getLogGroups(log_group_name_prefix=ut_arg2)
        # type test
        self.assertIs(type(actual), list)
        self.__loggroup_type_test(actual[0])
        # value test
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0]["retentionInDays"], expected)
        self.assertEqual(actual[0]["logGroupName"], expected2)

    def test_setRetentionDays2(self):
        ut_arg: int = 30
        expected: int = ut_arg
        setRetentionDays(days=ut_arg)
        actual: list = getLogGroups()
        self.assertIs(type(actual), list)
        for a in actual:
            # type test
            self.__loggroup_type_test(a)
            # value test
            self.assertEqual(a["retentionInDays"], expected)

    def __loggroup_type_test(self, loggroup: dict):
        self.assertIs(type(loggroup), dict)
        self.assertIs(type(loggroup["logGroupName"]), str)
        self.assertIs(type(loggroup["creationTime"]), int)
        self.assertIs(type(loggroup["retentionInDays"]), int)
        self.assertIs(type(loggroup["metricFilterCount"]), int)
        self.assertIs(type(loggroup["arn"]), str)
        self.assertIs(type(loggroup["storedBytes"]), int)
