# syntax=docker/dockerfile:1
FROM arm64v8/python:3

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/