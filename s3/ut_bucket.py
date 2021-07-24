import unittest
import json
import os

from bucket import Bucket


class UtEBucket(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        self.bucket = Bucket("tf-test-private-bucket")
        # create an ut file on local.
        f = open("./ut_test.txt", "w")
        f.write("this is unit test.")
        f.close()

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        # delete ut files on local.
        os.remove("./ut_test.json")
        os.remove("./ut_test.txt")

    def test_01_upload(self):
        ut_arg: str = "./ut_test.txt"
        ut_arg2: str = "ut/ut_test.txt"
        expected_result = None
        result = self.bucket.upload(ut_arg, ut_arg2)
        # value test
        self.assertEqual(result, expected_result)

    def test_02_create(self):
        ut_arg: str = "private"
        ut_arg2: str = json.dumps({"ut": "test"})
        ut_arg3: str = "ut/ut_test.json"
        expected_result = 200
        result = self.bucket.create(acl=ut_arg, body=ut_arg2, path=ut_arg3)
        # type test
        self.assertIs(type(result), dict)
        # value test
        self.assertEqual(result["ResponseMetadata"]["HTTPStatusCode"], expected_result)

    def test_03_ls(self):
        ut_arg: str = "ut/"
        expected_result = "ut/ut_test.json"
        expected_result2 = "ut/ut_test.txt"
        result = self.bucket.ls(path=ut_arg)
        # type test
        self.assertIs(type(result), list)
        # value test
        self.assertEqual(result[0]["Key"], expected_result)
        self.assertEqual(result[1]["Key"], expected_result2)

    def test_04_get(self):
        ut_arg: str = "ut/ut_test.json"
        expected_result = 200
        result = self.bucket.get(path=ut_arg)
        # type test
        self.assertIs(type(result), dict)
        # value test
        self.assertEqual(result["ResponseMetadata"]["HTTPStatusCode"], expected_result)

    def test_05_getContents(self):
        ut_arg: str = "ut/ut_test.json"
        expected_result = '{"ut": "test"}'
        result = self.bucket.getContents(path=ut_arg)
        # type test
        self.assertIs(type(result), str)
        # value test
        self.assertEqual(result, expected_result)

    def test_06_download(self):
        ut_arg: str = "./ut_test.json"
        ut_arg2: str = "ut/ut_test.json"
        expected_result = None
        result = self.bucket.download(local_path=ut_arg, s3_path=ut_arg2)
        # value test
        self.assertEqual(result, expected_result)

    def test_07_delete(self):
        ut_arg: str = "ut/ut_test.json"
        expected_result = 204
        result = self.bucket.delete(path=ut_arg)
        # type test
        self.assertIs(type(result), dict)
        # value test
        self.assertEqual(result["ResponseMetadata"]["HTTPStatusCode"], expected_result)


if __name__ == "__main__":
    unittest.main(failfast=True, exit=False)
