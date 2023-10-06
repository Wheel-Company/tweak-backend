# Use the official Python image as the base image
FROM arm64v8/ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get install -y nginx uwsgi python3 python3-pip wget locales supervisor
RUN apt-get install -y uwsgi-plugin-python3
RUN apt-get install -y libffi-dev 
RUN apt-get install -y libmysqlclient-dev

RUN rm /etc/nginx/sites-enabled/default
RUN mkdir /app

RUN sed -i -e 's/# ko_KR.UTF-8 UTF-8/ko_KR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG ko_KR.UTF-8  
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8 

WORKDIR /app

RUN sed -i '1 i\openssl_conf = default_conf' /etc/ssl/openssl.cnf
RUN echo '[default_conf]' >> /etc/ssl/openssl.cnf
RUN echo 'ssl_conf = ssl_sect' >> /etc/ssl/openssl.cnf
RUN echo '' >> /etc/ssl/openssl.cnf
RUN echo '[ssl_sect]' >> /etc/ssl/openssl.cnf
RUN echo 'system_default = system_default_sect' >> /etc/ssl/openssl.cnf
RUN echo '' >> /etc/ssl/openssl.cnf
RUN echo '[system_default_sect]' >> /etc/ssl/openssl.cnf
RUN echo 'MinProtocol = TLSv1' >> /etc/ssl/openssl.cnf
RUN echo 'CipherString = DEFAULT@SECLEVEL=1' >> /etc/ssl/openssl.cnf

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools

COPY ./requirements.txt /app
RUN python3 -m pip install -U -r requirements.txt
