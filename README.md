# aws-service-package

Python Packages as AWS Lambda Layers to operate AWS native services. They have basic functions or abstract classes of each service.

## how to install

```
pip install git+https://github.com/tomoki171923/aws-service-package
```

## unit test

```
docker-compose up unittest
```

## pre-commit

```
brew install pre-commit
pre-commit sample-config > .pre-commit-config.yaml
vi .pre-commit-config.yaml
pre-commit install
```
