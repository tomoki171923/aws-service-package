# aws-service-package

Python package. It helps operate AWS native services. It has basic functions or abstract classes of each service.

## For User

### Install

```
pip install git+https://github.com/tomoki171923/aws-service-package#egg=awspack
```

### Usage

```python
from awspack.s3.bucket import Bucket

if __name__ == "__main__":
    bucket = Bucket("tf-test-private-bucket")
    # upload a file in local into s3 bucket.
    bucket.upload("./file.txt", '20210101/file.tct')
```

## For Contributor

### Unit Test

```
docker-compose up unittest
```
