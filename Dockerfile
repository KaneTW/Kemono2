FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip libpq-dev curl
RUN pip3 install uwsgi

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

ENV LANG=C.UTF-8
CMD uwsgi --ini ./uwsgi.ini
