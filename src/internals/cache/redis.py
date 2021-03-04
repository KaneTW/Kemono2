import redis
from flask import current_app
from os import getenv

pool = None

def init():
    global pool
    pool = redis.ConnectionPool(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'))
    return pool

def get_conn():
    return redis.Redis(connection_pool=pool)
