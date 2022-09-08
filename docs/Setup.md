
# Setup

*How to use this project for yourself.*

<br>

1.  Clone the repository & switch to it's folder.
    
    ```sh
    git clone                                   \
        --recurse-submodules                    \
        https://github.com/OpenYiff/Kemono2.git \
        kemono-2
    
    cd kemono-2
    ```
    
    <br>

2.  Configure the setup.

    ```sh
    #   Archiver Config
    cp kitsune.py.example kitsune.py 
    
    #   Open .env + Configure
    cp .env.example .env 
    
    #   Open redis_map.py + Configure
    cp redis_map.py.example redis_map.py 
    
    #   Open flask.cfg + Set 'SECRET_KEY' Value
    cp flask.cfg.example flask.cfg
    ```
    
<br>