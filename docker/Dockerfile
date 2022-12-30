FROM nikolaik/python-nodejs:python3.8-nodejs16

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        curl \
        jq

RUN curl -L -O $(curl https://api.github.com/repos/tus/tusd/releases/latest -s | jq '.assets[] | select(.name=="tusd_linux_amd64.tar.gz") | .browser_download_url' -r)
RUN tar -O -zxvf tusd_linux_amd64.tar.gz tusd_linux_amd64/tusd > /usr/bin/tusd
RUN chmod +x /usr/bin/tusd

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

RUN npm install -g npm
RUN cd client && npm ci --also=dev && cd ..

ENV LANG=C.UTF-8

CMD python daemon.py
