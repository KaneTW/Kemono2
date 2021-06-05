from flask import g, current_app
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from os import getenv

pool = None

def init():
    global pool
    try:
        pool = psycopg2.pool.ThreadedConnectionPool(1, 2000,
            host = getenv('PGHOST'),
            dbname = getenv('PGDATABASE'),
            user = getenv('PGUSER'),
            password = getenv('PGPASSWORD'),
            port = getenv('PGPORT') or 5432,
            cursor_factory = RealDictCursor
        )
    except Exception as e:
        print(f"Unable to connect to the database: {e} ")

@contextmanager
def get_conn(key = None):
    try:
        with pool.getconn(key) as conn:
            yield conn
    except:
        raise
    finally:
        pool.putconn(conn, key)

@contextmanager
def get_cursor(key = None):
    try:
        with pool.getconn(key) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                yield cur
    except:
        raise
    finally:
        pool.putconn(conn, key)