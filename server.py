import re
from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from markupsafe import Markup
import psycopg2
from psycopg2 import pool
app = Flask(
    __name__,
    template_folder='views'
)
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.match(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)
try:
    pool = psycopg2.pool.SimpleConnectionPool(1, 20,
        host = getenv('PGHOST') if getenv('PGHOST') else 'localhost',
        dbname = getenv('PGDATABASE') if getenv('PGDATABASE') else 'kemonodb',
        user = getenv('PGUSER') if getenv('PGUSER') else 'nano',
        password = getenv('PGPASSWORD') if getenv('PGPASSWORD') else 'shinonome'
    )
except Exception as error:
    print("Failed to connect to the database: ",error)

@app.route('/')
def artists():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)
    if not request.args.get('commit'):
        results = {}
    else:
        connection = pool.getconn()
        cursor = connection.cursor()
        query = "SELECT * FROM lookup "
        query += "WHERE name ILIKE %s "
        params = ('%' + request.args.get('q') + '%',)
        if request.args.get('service'):
            query += "AND service = %s "
            params += (request.args.get('service'),)
        query += "AND service != 'discord-channel' "
        if request.args.get('sort_by') == 'indexed':
            query += 'ORDER BY indexed '
        elif request.args.get('sort_by') == 'name':
            query += 'ORDER BY name '
        elif request.args.get('sort_by') == 'service':
            query += 'ORDER BY service '
        if request.args.get('order') == 'asc':
            query += 'asc '
        elif request.args.get('order') == 'desc':
            query += 'desc '
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params += (offset,)
        query += "LIMIT 25"
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        if connection:
            pool.putconn(connection)
    return render_template(
        'artists.html',
        props = props,
        results = results,
        base = base
    )

@app.route('/artists')
def root():
    return redirect('/', code=308)

@app.route('/artists/random')
def random_artist():
    connection = pool.getconn()
    cursor = connection.cursor()
    query = "SELECT id, service FROM lookup WHERE service != 'discord-channel' ORDER BY random() LIMIT 1"
    cursor.execute(query)
    random = cursor.fetchall()
    cursor.close()
    if connection:
        pool.putconn(connection)
    if len(random) == 0:
        return redirect('back')
    return redirect(f'/{random[0][1]}/user/{random[0][0]}')

@app.route('/artists/updated')
def updated_artists():
    connection = pool.getconn()
    cursor = connection.cursor()
    props = {
        'currentPage': 'artists'
    }
    query = 'WITH "posts" as (select "user", "service", max("added") from "booru_posts" group by "user", "service" order by max(added) desc limit 50) '\
        'select "user", "posts"."service", "lookup"."name", "max" from "posts" inner join "lookup" on "posts"."user" = "lookup"."id"'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    if connection:
        pool.putconn(connection)
    return render_template(
        'updated.html',
        props = props,
        results = results
    )

@app.route('/artists/favorites')
def favorites():
    props = {
        'currentPage': 'artists'
    }
    return render_template(
        'favorites.html',
        props = props
    )

@app.route('/posts')
def posts():
    connection = pool.getconn()
    cursor = connection.cursor()
    props = {
        'currentPage': 'posts'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    query = "SELECT * FROM booru_posts ORDER BY added desc "
    params = ()

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and request.args.get('limit') <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()

    if connection:
        pool.putconn(connection)
    return render_template(
        'posts.html',
        props = props,
        results = results,
        base = base
    )

@app.route('/posts/random')
def random_post():
    connection = pool.getconn()
    cursor = connection.cursor()
    query = "SELECT service, \"user\", id FROM booru_posts WHERE random() < 0.01 LIMIT 1"
    cursor.execute(query)
    random = cursor.fetchall()
    cursor.close()
    if connection:
        pool.putconn(connection)
    return redirect(f'/{random[0][0]}/user/{random[0][1]}/post/{random[0][2]}')

@app.route('/files/<path>')
def files(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'files'), path)

@app.route('/attachments/<path>')
def attachments(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'attachments'), path)

@app.route('/inline/<path>')
def inline(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'inline'), path)