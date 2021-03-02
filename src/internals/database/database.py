from flask import g, current_app
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from os import getenv

def make_pool():
    pool = None
    try:
        pool = psycopg2.pool.SimpleConnectionPool(1, 2000,
            host = getenv('PGHOST'),
            dbname = getenv('PGDATABASE'),
            user = getenv('PGUSER'),
            password = getenv('PGPASSWORD'),
            cursor_factory = RealDictCursor
        )
    except Exception as error:
        print("Failed to connect to the database: ", error)
    return pool

def get_pool():
    return current_app.config['DATABASE_POOL']

def get_cursor():
    pool = current_app.config['DATABASE_POOL']
    if 'cursor' not in g:
        g.connection = pool.getconn()
        g.cursor = g.connection.cursor()
    return g.cursor
