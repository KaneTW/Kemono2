import psycopg2

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor
from flask import g, current_app
from typing import Optional
from threading import Lock
from os import getenv

from src.config import Configuration

pool: Optional[ThreadedConnectionPool] = None
connection_lock = Lock()


def init():
    global pool
    try:
        pool = ThreadedConnectionPool(
            1,
            2000,
            host=Configuration().database['host'],
            dbname=Configuration().database['database'],
            user=Configuration().database['user'],
            password=Configuration().database['password'],
            port=Configuration().database['port'],
            cursor_factory=RealDictCursor
        )
    except Exception as error:
        print("Failed to connect to the database: ", error)
    return pool


def get_pool():
    return pool


def get_cursor() -> cursor:
    if 'cursor' not in g:
        g.connection = pool.getconn()
        g.cursor = g.connection.cursor()
    return g.cursor
