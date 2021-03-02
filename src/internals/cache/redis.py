import redis
from flask import current_app
from os import getenv

def make_pool():
    return redis.ConnectionPool(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'))

def get_conn():
    return redis.Redis(connection_pool=current_app.config['REDIS_POOL'])
