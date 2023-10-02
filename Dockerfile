# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.8-slim-buster as build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/