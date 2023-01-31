FROM nikolaik/python-nodejs:python3.8-nodejs16

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        curl \
        jq

RUN curl -L -O $(curl https://api.github.com/repos/tus/tusd/releases/latest -s | jq '.assets[] | select(.name=="tusd_linux_amd64.tar.gz") | .browser_download_url' -r); \
    tar -xvf tusd_linux_amd64.tar.gz -C /usr/local/bin/ --strip-components=1 tusd_linux_amd64/tusd; \
    chmod +x /usr/local/bin/tusd; \
    rm tusd_linux_amd64.tar.gz

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

RUN npm install -g npm
RUN cd client && npm ci --also=dev && cd ..

ENV LANG=C.UTF-8

CMD python daemon.py
