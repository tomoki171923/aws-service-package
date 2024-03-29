FROM python:3.9-slim

WORKDIR /usr/src/app

COPY Pipfile ./

RUN apt-get update \
    && apt-get -y install locales git \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --upgrade pipenv \
    && pipenv install

COPY . .
