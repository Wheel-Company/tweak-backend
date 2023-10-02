# syntax=docker/dockerfile:1
FROM python:3.11.5-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get -qq update
RUN pip3 --quiet install --requirement requirements.txt \
         --force-reinstall --upgrade
COPY . /app/