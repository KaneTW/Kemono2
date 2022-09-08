
# Develop

For now Docker is a primary way of working on the repo.

<br>

## Installation

<br>

1.  Create a virtual environment.
    
    ```sh
    #   Install the package if it's not installed
    pip install virtualenv
    
    #   Make it easier to manage python versions
    virtualenv --upgrade-embed-wheels
    virtualenv --python 3.8 venv
    ```
    
    <br>

2.  Activate the virtual environment.
    
    ```sh
    #   Windows ➞ venv\Scripts\activate
    source venv/bin/activate
    ```
    
    <br>

3.  Install python packages.

    ```sh
    pip install \
        --requirement requirements.txt
    ```
    
    <br>

4.  Install  `pre-commit`  hooks.

    ```sh
    pre-commit install --install-hooks
    ````

<br>
<br>

## IDE

*IDE specific instructions.*

<br>

### VSCode

<br>

1.  Copy  `.code-workspace`  file.

    ```sh
    cp                                              \
        configs/workspace.code-workspace.example    \
        kemono-2.code-workspace
    ```
    
    <br>
    
2.  Install the recommended extensions.

<br>
<br>

## Docker

<br>

```sh
docker-compose --file docker-compose.dev.yml build
docker-compose --file docker-compose.dev.yml up
```

<br>

In a browser, visit  [`http://localhost:5000/`]

<br>

### Database

<br>

1.  Register an account.

2.  Visit  [`http://localhost:5000/development`]

3.  Click either seeded or random generation.
    
    *This will start a mock import process,* <br>
    *which will also populate the database.*

<br>

### Files

TBD

<br>

### Build

```sh
docker-compose build
docker-compose up --detach
```

<br>

In a browser, visit  [`http://localhost:8000/`]

<br>
<br>

## Manual

> **TODO** : Write installation and setup instructions

<br>

This assumes you have  `Python 3.8+`  &  `Node 12+`  installed <br>
as well as a running **PostgreSQL** server with **Pgroonga**.

<br>

```sh
#   Make sure your database is initialized
#   cd to kemono directory

pip install virtualenv
virtualenv venv

#   Windows ➞ venv\Scripts\activate 
source venv/bin/activate

pip install \
    --requirement requirements.txt

cd client               \
    && npm install      \
    && npm run build    \
    && cd ..

#   Open .env + Configure
cp .env.example .env

#   Open flask.cfg + Configure
cp flask.cfg.example flask.cfg

set FLASK_APP=server.py
set FLASK_ENV=development

flask run
```

<br>


<!----------------------------------------------------------------------------->

[`http://localhost:5000/development`]: http://localhost:5000/development
[`http://localhost:5000/`]: http://localhost:5000/
[`http://localhost:8000/`]: http://localhost:8000/