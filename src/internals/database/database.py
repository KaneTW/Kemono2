from os import getenv
from flask import g, current_app
from threading import Lock
import psycopg2
from psycopg2 import pool
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor

from typing import Optional
from psycopg2.extensions import cursor

pool: Optional[ThreadedConnectionPool] = None
connection_lock = Lock()

def init():
    global pool
    try:
        pool = ThreadedConnectionPool(1, 2000,
            host = getenv('PGHOST'),
            dbname = getenv('PGDATABASE'),
            user = getenv('PGUSER'),
            password = getenv('PGPASSWORD'),
            port = getenv('PGPORT', '5432'),
            cursor_factory = RealDictCursor
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
