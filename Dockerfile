# Use the official Python image as the base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get install -y nginx uwsgi python3 python3-pip wget locales supervisor
RUN apt-get install -y uwsgi-plugin-python3
RUN apt-get install -y libffi-dev 
RUN apt-get install -y libmysqlclient-dev

# # 필수 패키지 설치
# RUN apt-get update && apt-get install -yq software-properties-common  \
#     wget  \
#     build-essential  \
#     libssl-dev  \
#     libbz2-dev  \
#     libffi-dev  \
#     zlib1g-dev  \
#     libsqlite3-dev  \
#     tzdata  \
#     libbluetooth-dev \
#     tk-dev \
#     uuid-dev \
#     && \
#     ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
#     dpkg-reconfigure --frontend noninteractive tzdata

# Install core dependencies.
# RUN apt-get update && apt-get install -y libpq-dev build-essential

# # Set the working directory in the container
# WORKDIR /app
# # Copy the application code to the container
# COPY . /app

# # Python 3.11.4 다운로드 및 설치
# RUN wget https://www.python.org/ftp/python/${python_version}/Python-${python_version}.tgz && \
#     tar xzf Python-${python_version}.tgz && \
#     cd Python-${python_version} && \
#     ./configure --prefix=/usr/local --enable-optimizations && \
#     make altinstall

# #RUN pip install --no-cache-dir --upgrade pip

# # 기본 python 커맨드를 Python 3.11.4 버전으로 설정
# RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 && \
#     update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1 && \
#     update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3.11 1

# RUN set -xe && apt-get -yqq update && apt-get -yqq install python3-pip
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

# Install the required packages
# RUN python -m pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the port that your Django application will run on
# EXPOSE 8000

# # Start the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
