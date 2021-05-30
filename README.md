# Kemono project

## Setup
```sh
git clone https://github.com/OpenYiff/Kemono2.git kemono-2
cd kemono-2
cp .env.example .env # open .env and configure
cp flask.cfg.example flask.cfg # open flask.cfg and configure
```
## Docker
```sh
cp kitsune.py.example kitsune.py # open kitsune.py and configure
```

### Develop
```sh
docker-compose --file docker-compose.dev.yml build
docker-compose --file docker-compose.dev.yml up
```
Open `http://localhost:5000/` in the browser.

### Build
```sh
docker-compose build
docker-compose up --detach
```

Open `http://localhost:8000/` in the browser.

## Manual
TODO: write installation and setup instructions

This assumes you have Python 3, Node 12+ installed and a running PostgreSQL server.
```sh
# make sure your database is initialized
# cd to kemono directory
pip install virtualenv
virtualenv venv
source venv/bin/activate # venv\Scripts\activate on Windows
pip install --requirement requirements.txt
cd client && npm install && npm run build && cd ..
cp .env.example .env # open .env and configure
cp flask.cfg.example flask.cfg # open flask.cfg and configure
set FLASK_APP=server.py
set FLASK_ENV=development
flask run
```