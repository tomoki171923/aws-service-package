import unittest
import json
import os

from src.awspack.s3.s3 import S3
from src.awspack.s3.bucket import Bucket


class UtEBucket(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        self.bucket_name: str = "ut-s3-bucket"
        self.s3 = S3()
        s3_arg: dict = {"Bucket": self.bucket_name}
        s3_arg["ACL"] = "private"
        s3_arg["CreateBucketConfiguration"] = {"LocationConstraint": "us-east-1"}
        self.s3.createBucket(s3_arg)
        self.bucket = Bucket(self.bucket_name)
        # create an ut file on local.
        f = open("test/ut_test.txt", "w")
        f.write("this is unit test.")
        f.close()

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        # delete ut files on local.
        os.remove("./test/ut_test.json")
        os.remove("test/ut_test.txt")
        s3_arg: dict = {"Bucket": self.bucket_name}
        self.s3.deleteBucket(s3_arg)

    def test_01_upload(self):
        ut_arg: str = "test/ut_test.txt"
        ut_arg2: str = "test/ut_test.txt"
        expected = None
        actual = self.bucket.upload(ut_arg, ut_arg2)
        # value test
        self.assertEqual(actual, expected)

    def test_02_create(self):
        ut_arg: str = "private"
        ut_arg2: str = json.dumps({"ut": "test"})
        ut_arg3: str = "test/ut_test.json"
        expected = 200
        actual = self.bucket.create(acl=ut_arg, body=ut_arg2, path=ut_arg3)
        # type test
        self.assertIs(type(actual), dict)
        # value test
        self.assertEqual(actual["ResponseMetadata"]["HTTPStatusCode"], expected)

    def test_03_ls(self):
        ut_arg: str = "test/"
        expected = "test/ut_test.json"
        expected2 = "test/ut_test.txt"
        actual = self.s3.ls(bucket_name=self.bucket_name, path=ut_arg)
        # type test
        self.assertIs(type(actual), list)
        # value test
        self.assertEqual(actual[0]["Key"], expected)
        self.assertEqual(actual[1]["Key"], expected2)

    def test_04_get(self):
        ut_arg: str = "test/ut_test.json"
        expected = 200
        actual = self.bucket.get(path=ut_arg)
        # type test
        self.assertIs(type(actual), dict)
        # value test
        self.assertEqual(actual["ResponseMetadata"]["HTTPStatusCode"], expected)

    def test_05_getContents(self):
        ut_arg: str = "test/ut_test.json"
        expected = '{"ut": "test"}'
        actual = self.bucket.getContents(path=ut_arg)
        # type test
        self.assertIs(type(actual), str)
        # value test
        self.assertEqual(actual, expected)

    def test_06_download(self):
        ut_arg: str = "./test/ut_test.json"
        ut_arg2: str = "test/ut_test.json"
        expected = None
        actual = self.bucket.download(local_path=ut_arg, s3_path=ut_arg2)
        # value test
        self.assertEqual(actual, expected)

    def test_07_delete(self):
        ut_arg: str = "test/ut_test.json"
        expected = 204
        actual = self.bucket.delete(path=ut_arg)
        # type test
        self.assertIs(type(actual), dict)
        # value test
        self.assertEqual(actual["ResponseMetadata"]["HTTPStatusCode"], expected)

    def test_08_delete(self):
        ut_arg: str = "test/ut_test.txt"
        expected = 204
        actual = self.bucket.delete(path=ut_arg)
        # type test
        self.assertIs(type(actual), dict)
        # value test
        self.assertEqual(actual["ResponseMetadata"]["HTTPStatusCode"], expected)
