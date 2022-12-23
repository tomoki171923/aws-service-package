import unittest
from src.awspack.s3.s3 import S3


class UtS3BucketSelect(unittest.TestCase):

    # constructor of unittest class
    @classmethod
    def setUpClass(self):
        self.bucket_name: str = "ut-s3-bucket-select"
        self.s3 = S3()

    # destructor of unittest class
    @classmethod
    def tearDownClass(self):
        pass

    def test_01_select_no_format(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.jsonl",
            "InputSerialization": {
                "JSON": {
                    "Type": "LINES",
                }
            },
            "OutputSerialization": {
                "JSON": {
                    "RecordDelimiter": "\n",
                }
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s",
        }
        actual = self.s3.select(ut_arg, format=False)
        # type test
        self.assertIs(type(actual), dict)
        # value test
        self.assertEqual(actual["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_02_select_jsonl(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.jsonl.gz",
            "InputSerialization": {
                "CompressionType": "GZIP",
                "JSON": {
                    "Type": "LINES",
                },
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.__json_data_type_test(actual)
        # value test
        self.assertIs(len(actual), 3)

    def test_03_select_json(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.json",
            "InputSerialization": {
                "JSON": {
                    "Type": "DOCUMENT",
                }
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), dict)
        self.assertIs(type(actual["people"]), list)
        self.__json_data_type_test(actual["people"])
        # value test
        self.assertIs(len(actual["people"]), 3)

    def test_04_select_csv(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.csv",
            "InputSerialization": {
                "CompressionType": "NONE",
                "CSV": {
                    "FileHeaderInfo": "USE",
                    "RecordDelimiter": "\n",
                    "FieldDelimiter": ",",
                },
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s LIMIT 5",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.__csv_data_type_test(actual)
        # value test
        self.assertIs(len(actual), 5)

    def test_05_select_where_jsonl(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.jsonl.gz",
            "InputSerialization": {
                "CompressionType": "GZIP",
                "JSON": {
                    "Type": "LINES",
                },
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s WHERE s.gender = 'male' ",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.__json_data_type_test(actual)
        # value test
        self.assertIs(len(actual), 2)
        for i in range(len(actual)):
            self.assertEqual(actual[i]["gender"], "male")

    def test_06_select_where_jsonl(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.jsonl.gz",
            "InputSerialization": {
                "CompressionType": "GZIP",
                "JSON": {
                    "Type": "LINES",
                },
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s WHERE s.gender = 'male' AND s.age > 30 ",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.__json_data_type_test(actual)
        # value test
        self.assertIs(len(actual), 1)
        self.assertEqual(actual[0]["gender"], "male")
        self.assertGreaterEqual(actual[0]["age"], 30)

    def test_07_select_where_jsonl(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.jsonl.gz",
            "InputSerialization": {
                "CompressionType": "GZIP",
                "JSON": {
                    "Type": "LINES",
                },
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s WHERE s.number = '7349282382' OR s.number = '456754675' ",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.__json_data_type_test(actual)
        # value test
        self.assertIs(len(actual), 2)
        self.assertEqual(actual[0]["number"], "7349282382")
        self.assertEqual(actual[1]["number"], "456754675")

    def test_08_select_where_csv(self):
        ut_arg: dict = {
            "Bucket": self.bucket_name,
            "Key": "sample/sample.csv",
            "InputSerialization": {
                "CompressionType": "NONE",
                "CSV": {
                    "FileHeaderInfo": "USE",
                    "RecordDelimiter": "\n",
                    "FieldDelimiter": ",",
                },
            },
            "ExpressionType": "SQL",
            "Expression": "SELECT * FROM s3object s WHERE s.Email = 'mconley@example.net' ",
        }
        actual = self.s3.select(ut_arg)
        # type test
        self.assertIs(type(actual), list)
        self.__csv_data_type_test(actual)
        # value test
        # self.assertIs(len(actual), 1)
        self.assertEqual(actual[0]["Email"], "mconley@example.net")

    def __json_data_type_test(self, data: list):
        for i in range(len(data)):
            self.assertIs(type(data[i]), dict)
            self.assertIs(type(data[i]["firstName"]), str)
            self.assertIs(type(data[i]["lastName"]), str)
            self.assertIs(type(data[i]["gender"]), str)
            self.assertIs(type(data[i]["age"]), int)
            self.assertIs(type(data[i]["number"]), str)

    def __csv_data_type_test(self, data: list):
        for i in range(len(data)):
            self.assertIs(type(data[i]), dict)
            self.assertIs(type(data[i]["Index"]), str)
            self.assertIs(type(data[i]["User Id"]), str)
            self.assertIs(type(data[i]["First Name"]), str)
            self.assertIs(type(data[i]["Last Name"]), str)
            self.assertIs(type(data[i]["Sex"]), str)
            self.assertIs(type(data[i]["Email"]), str)
            self.assertIs(type(data[i]["Phone"]), str)
            self.assertIs(type(data[i]["Date of birth"]), str)
            self.assertIs(type(data[i]["Job Title"]), str)
