# aws-service-package

Python Packages as AWS Lambda Layers to operate AWS native services. They have basic functions or abstract classes of each service.

## unit test

```
docker-compose up
python -m unittest discover -s tests -p "ut_dynamodb_database.py"
```

or

```
(local)
docker-compose run --rm py38 bash
(container)
vi ~/.aws/credentials
export AWS_PROFILE=xxx
python -m unittest discover -s tests -p "ut_*.py"
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
