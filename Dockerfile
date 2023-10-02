# syntax=docker/dockerfile:1
FROM ubuntu:22.04
RUN apt-get -y update
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmysqlclient-dev
FROM python:3.11.5-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/