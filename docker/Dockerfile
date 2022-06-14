FROM nikolaik/python-nodejs:python3.8-nodejs16

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        curl

WORKDIR /app

COPY requirements.txt requirements.txt

RUN npm install -g npm
RUN npm ci --also=dev
RUN pip3 install -r requirements.txt

COPY . /app

ENV LANG=C.UTF-8

CMD python daemon.py
