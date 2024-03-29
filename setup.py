from setuptools import setup, find_packages
from glob import glob
from os.path import basename
from os.path import splitext

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="awspack",
    version_config=True,
    setup_requires=["setuptools-git-versioning"],
    author="tomoki",
    url="https://github.com/tomoki171923/aws-service-package",
    description="this package helps operate AWS native services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "boto3>=1.18",
        "pyutil @ git+https://github.com/tomoki171923/python-util.git#egg=pyutil",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
)
