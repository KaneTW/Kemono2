

## Setup
1. Clone repo and switch to the repo folder:
    ```sh
    git clone --recurse-submodules https://github.com/OpenYiff/Kemono2.git kemono-2
    cd kemono-2
    ```

2. Set up configs:
    ```sh
    cp kitsune.py.example kitsune.py # archiver config
    cp .env.example .env # open .env and configure
    cp redis_map.py.example redis_map.py # open redis_map.py and configure
    cp flask.cfg.example flask.cfg # open flask.cfg and set 'SECRET_KEY' value
    ```