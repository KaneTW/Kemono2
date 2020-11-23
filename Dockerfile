FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx libpq-dev libev-dev python-pkg-resources

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

ENV DB_ROOT=/storage
CMD python3 -c "from server import app; import bjoern; bjoern.run(app, '0.0.0.0', 8000)"