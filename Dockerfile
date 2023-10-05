# Use the official Python image as the base image
FROM ubuntu:20.04 as python_builder

ARG python_version=3.11.4
ARG python_major_version
ENV DEBIAN_FRONTEND=noninteractive

# 필수 패키지 설치
RUN apt-get update && apt-get install -yq software-properties-common  \
    wget  \
    build-essential  \
    libssl-dev  \
    libbz2-dev  \
    libffi-dev  \
    zlib1g-dev  \
    libsqlite3-dev  \
    tzdata  \
    libbluetooth-dev \
    tk-dev \
    uuid-dev \
    && \
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Set the working directory in the container
WORKDIR /app
# Copy the application code to the container
COPY . /app

# Python 3.11.4 다운로드 및 설치
RUN wget https://www.python.org/ftp/python/${python_version}/Python-${python_version}.tgz && \
    tar xzf Python-${python_version}.tgz && \
    cd Python-${python_version} && \
    ./configure --prefix=/usr/local --enable-optimizations && \
    make altinstall

#RUN pip install --no-cache-dir --upgrade pip

# 기본 python 커맨드를 Python 3.11.4 버전으로 설정
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3.11 1

RUN set -xe && apt-get -yqq update && apt-get -yqq install python3-pip

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your Django application will run on
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
