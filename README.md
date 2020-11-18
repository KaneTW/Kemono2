TODO: write actual README
## Setup
This assumes you have Python 3 installed and a running PostgreSQL server.
```sh
# cd to kemono directory
pip install virtualenv
virtualenv venv
source venv/bin/activate # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env # open .env and change settings
set FLASK_APP=server.py
set FLASK_ENV=development
flask run
```