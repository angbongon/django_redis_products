FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN python -m pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN apt-get update && apt-get install -y build-essential redis-server

RUN adduser user
USER user
