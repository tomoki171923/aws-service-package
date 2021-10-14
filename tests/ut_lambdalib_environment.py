import unittest
import json
import os

from src.service.lambdalib.environment import (
    isDevOrSt,
    isLocal,
    isDocker,
    isPro,
    isSt,
    isDev,
)


class UtLambdalibEnvironment(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        pass

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        pass

    def test_isDev(self):
        expected: bool = False
        actual: bool = isDev()
        self.assertIs(type(actual), bool)
        self.assertEqual(actual, expected)
        os.environ["AWS_LAMBDA_FUNCTION_VERSION"] = "$LATEST"
        expected2: bool = True
        actual2: bool = isDev()
        self.assertEqual(actual2, expected2)
        self.assertIs(type(actual2), bool)

    def test_isSt(self):
        expected: bool = False
        actual: bool = isSt()
        self.assertIs(type(actual), bool)
        self.assertEqual(actual, expected)
        os.environ["AWS_LAMBDA_FUNCTION_ALIAS"] = "st"
        expected2: bool = True
        actual2: bool = isSt()
        self.assertEqual(actual2, expected2)
        self.assertIs(type(actual2), bool)

    def test_isPro(self):
        expected: bool = False
        actual: bool = isPro()
        self.assertIs(type(actual), bool)
        self.assertEqual(actual, expected)
        os.environ["AWS_LAMBDA_FUNCTION_ALIAS"] = "pro"
        expected2: bool = True
        actual2: bool = isPro()
        self.assertEqual(actual2, expected2)
        self.assertIs(type(actual2), bool)

    def test_isDevOrSt(self):
        os.environ["AWS_LAMBDA_FUNCTION_ALIAS"] = "pro"
        os.environ["AWS_LAMBDA_FUNCTION_VERSION"] = "21"
        expected: bool = False
        actual: bool = isDevOrSt()
        self.assertIs(type(actual), bool)
        self.assertEqual(actual, expected)
        os.environ["AWS_LAMBDA_FUNCTION_ALIAS"] = "st"
        expected2: bool = True
        actual2: bool = isDevOrSt()
        self.assertEqual(actual2, expected2)
        self.assertIs(type(actual2), bool)
        os.environ.pop("AWS_LAMBDA_FUNCTION_ALIAS", None)
        os.environ["AWS_LAMBDA_FUNCTION_VERSION"] = "$LATEST"
        expected3: bool = True
        actual3: bool = isDevOrSt()
        self.assertEqual(actual3, expected3)
        self.assertIs(type(actual3), bool)

    def test_isLocal(self):
        os.environ.pop("AWS_LAMBDA_FUNCTION_VERSION", None)
        expected: bool = True
        actual: bool = isLocal()
        self.assertIs(type(actual), bool)
        self.assertEqual(actual, expected)
        os.environ["AWS_LAMBDA_FUNCTION_VERSION"] = "$LATEST"
        expected2: bool = False
        actual2: bool = isLocal()
        self.assertEqual(actual2, expected2)
        self.assertIs(type(actual2), bool)
        os.environ["AWS_LAMBDA_ENV"] = "local"
        expected3: bool = True
        actual3: bool = isLocal()
        self.assertEqual(actual3, expected3)
        self.assertIs(type(actual3), bool)

    def test_isDocker(self):
        expected: bool = True
        actual: bool = isDocker()
        self.assertIs(type(actual), bool)
        self.assertEqual(actual, expected)
