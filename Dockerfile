FROM python:3.10-buster as builder

COPY requirements.txt requirements.txt

RUN set -ex && pip install --upgrade pip

RUN set -ex && pip install -r requirements.txt
RUN set -ex && pip install rdkit-pypi==2022.3.2.1

FROM builder as final

WORKDIR /app

COPY . /app

EXPOSE 8000
