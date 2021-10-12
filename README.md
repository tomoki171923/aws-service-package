# aws-service-package

Python Packages as AWS Lambda Layers to operate AWS native services. They have basic functions or abstract classes of each service.

```
root
 └ cloudwatch  ... for AWS Cloudwatch.
 └ common  ... for AWS Lambda.
 └ dynamodb  ... for AWS DynamoDB.
 └ s3  ... for AWS S3.
 └ ses  ... for AWS SES.
 └ sns  ... for AWS SNS.
```

## unit test

```
(e.g.)
cd s3
python ut_bucket.py
```

## code format

```
find . -type f -name "*.py" | xargs black
```

## code lint

```
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

## pre-commit

```
brew install pre-commit
pre-commit sample-config > .pre-commit-config.yaml
vi .pre-commit-config.yaml
pre-commit install
```
