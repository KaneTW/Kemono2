## Develop
For now Docker is a primary way of working on the repo.

### Installation
1. Create a virtual environment:
    ```sh
    pip install virtualenv # install the package if it's not installed
    virtualenv --upgrade-embed-wheels # makes it easier to manage python versions
    virtualenv --python 3.8 venv
    ```

2. Activate the virtual environment:
    ```sh
    source venv/bin/activate # venv\Scripts\activate on Windows
    ```

3. Install python packages:
    ```sh
    pip install --requirement requirements.txt
    ```

4. Install `pre-commit` hooks:
    ```sh
    pre-commit install --install-hooks
    ````

### IDE-specific

#### VSCode
Copy `.code-workspace` file:
```sh
cp configs/workspace.code-workspace.example kemono-2.code-workspace
```
And install recommended extensions.

### Docker
```sh
docker-compose --file docker-compose.dev.yml build
docker-compose --file docker-compose.dev.yml up
```
Open `http://localhost:5000/` in the browser.

#### Database
1. Register an account.
2. Visit `http://localhost:5000/development`.
3. Click either seeded or random generation.
4. This will start a mock import process, which will also populate the database.

#### Files
TBD

#### Build
```sh
docker-compose build
docker-compose up --detach
```

Open `http://localhost:8000/` in the browser.

### Manual
TODO: write installation and setup instructions

This assumes you have Python 3.8+ Node 12+ installed and a running PostgreSQL server with Pgroonga.
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