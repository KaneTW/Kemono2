import re
from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

from routes.help import help_app
from routes.proxy import proxy_app

from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, make_response, g, abort
from flask_caching import Cache
from markupsafe import Markup
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from hashlib import sha256

app = Flask(
    __name__,
    template_folder='views'
)
app.config.from_pyfile('flask.cfg')
cache = Cache(app)
app.url_map.strict_slashes = False
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.search(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)
app.register_blueprint(help_app, url_prefix='/help')
app.register_blueprint(proxy_app, url_prefix='/proxy')
try:
    pool = psycopg2.pool.SimpleConnectionPool(1, 20,
        host = getenv('PGHOST') if getenv('PGHOST') else 'localhost',
        dbname = getenv('PGDATABASE') if getenv('PGDATABASE') else 'kemonodb',
        user = getenv('PGUSER') if getenv('PGUSER') else 'nano',
        password = getenv('PGPASSWORD') if getenv('PGPASSWORD') else 'shinonome',
        cursor_factory = RealDictCursor
    )
except Exception as error:
    print("Failed to connect to the database: ",error)

def make_cache_key(*args,**kwargs):
    return request.full_path

@app.before_request
def clear_trailing():
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        response = redirect(rp[:-1])
        response.autocorrect_location_header = False
        return response

def get_cursor():
    if 'cursor' not in g:
        g.connection = pool.getconn()
        g.cursor = g.connection.cursor()
    return g.cursor

@app.teardown_appcontext
def close(e):
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()
        connection = g.pop('connection', None)
        connection.commit()
        if connection is not None:
            pool.putconn(connection)

@app.route('/')
@cache.cached(key_prefix=make_cache_key)
def artists():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)
    if not request.args.get('commit'):
        results = {}
    else:
        query = "SELECT * FROM lookup "
        query += "WHERE name ILIKE %s "
        params = ('%' + request.args.get('q') + '%',)
        if request.args.get('service'):
            query += "AND service = %s "
            params += (request.args.get('service'),)
        query += "AND service != 'discord-channel' "
        query += "ORDER BY " + {
            'indexed': 'indexed',
            'name': 'name',
            'service': 'service'
        }.get(request.args.get('sort_by'), 'indexed')
        query += {
            'asc': ' asc ',
            'desc': ' desc '
        }.get(request.args.get('order'), 'asc')
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params += (offset,)
        query += "LIMIT 25"

        cursor = get_cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
    response = make_response(render_template(
        'artists.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/artists')
def root():
    response = redirect('/', code=308)
    response.autocorrect_location_header = False
    return response

@app.route('/artists/random')
def random_artist():
    cursor = get_cursor()
    query = "SELECT id, service FROM lookup WHERE service != 'discord-channel' ORDER BY random() LIMIT 1"
    cursor.execute(query)
    random = cursor.fetchall()
    if len(random) == 0:
        return redirect('back')
    response = redirect(url_for('user', service = random[0]['service'], id = random[0]['id']))
    response.autocorrect_location_header = False
    return response

@app.route('/artists/updated')
@cache.cached(key_prefix=make_cache_key)
def updated_artists():
    cursor = get_cursor()
    props = {
        'currentPage': 'artists'
    }
    query = 'WITH "posts" as (select "user", "service", max("added") from "booru_posts" group by "user", "service" order by max(added) desc limit 50) '\
        'select "user", "posts"."service" as service, "lookup"."name" as name, "max" from "posts" inner join "lookup" on "posts"."user" = "lookup"."id"'
    cursor.execute(query)
    results = cursor.fetchall()
    response = make_response(render_template(
        'updated.html',
        props = props,
        results = results
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/artists/favorites')
def favorites():
    props = {
        'currentPage': 'artists'
    }
    response = make_response(render_template(
        'favorites.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=300, public, stale-while-revalidate=2592000'
    return response

@app.route('/posts')
@cache.cached(key_prefix=make_cache_key)
def posts():
    cursor = get_cursor()
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

    response = make_response(render_template(
        'posts.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/posts/upload')
def upload_post():
    props = {
        'currentPage': 'posts'
    }
    response = make_response(render_template(
        'upload.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/posts/random')
def random_post():
    cursor = get_cursor()
    query = "SELECT service, \"user\", id FROM booru_posts WHERE random() < 0.01 LIMIT 1"
    cursor.execute(query)
    random = cursor.fetchall()
    response = redirect(url_for('post', service = random[0]['service'], id = random[0]['user'], post = random[0]['id']))
    response.autocorrect_location_header = False
    return response

@app.route('/files/<path>')
def files(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'files'), path)

@app.route('/attachments/<path>')
def attachments(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'attachments'), path)

@app.route('/inline/<path>')
def inline(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'inline'), path)

@app.route('/requests/images/<path>')
def request_image(path):
    return send_from_directory(join(getenv('DB_ROOT'), 'requests/images'), path)

# TODO: /:service/user/:id/rss

@app.route('/<service>/user/<id>')
@cache.cached(key_prefix=make_cache_key)
def user(service, id):
    cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'id': id,
        'service': service
    }
    base = request.args.to_dict()
    base.pop('o', None)
    base["service"] = service
    base["id"] = id

    query = "SELECT * FROM booru_posts WHERE \"user\" = %s AND service = %s ORDER BY published desc "
    params = (id, service)

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor2 = get_cursor()
    query2 = "SELECT id FROM booru_posts WHERE \"user\" = %s AND service = %s GROUP BY id"
    params2 = (id, service)
    cursor2.execute(query2, params2)
    results2 = cursor2.fetchall()
    props["count"] = len(results2)

    response = make_response(render_template(
        'user.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/<service>/user/<id>/post/<post>')
@cache.cached(key_prefix=make_cache_key)
def post(service, id, post):
    cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'service': service if service else 'patreon'
    }
    query = 'SELECT * FROM booru_posts '
    query += 'WHERE id = %s '
    params = (post,)
    query += 'AND booru_posts.user = %s '
    params += (id,)
    query += 'AND service = %s '
    params += (service,)
    query += 'ORDER BY added asc'

    cursor.execute(query, params)
    results = cursor.fetchall()

    result_previews = []
    result_attachments = []
    for post in results:
        previews = []
        attachments = []
        if len(post['file']):
            if re.search("\.(gif|jpe?g|png|webp)$", post['file']['path'], re.IGNORECASE):
                previews.append({
                    'type': 'thumbnail',
                    'path': post['file']['path'].replace('https://kemono.party','')
                })
            else:
                attachments.append({
                    'path': post['file']['path'],
                    'name': post['file']['name']
                })
        if len(post['embed']):
            previews.append({
                'type': 'embed',
                'url': post['embed']['url'],
                'subject': post['embed']['subject'],
                'description': post['embed']['description']
            })
        for attachment in post['attachments']:
            if re.search("\.(gif|jpe?g|png|webp)$", attachment['path'], re.IGNORECASE):
                previews.append({
                    'type': 'thumbnail',
                    'path': attachment['path'].replace('https://kemono.party','')
                })
            else:
                attachments.append({
                    'path': attachment['path'],
                    'name': attachment['name']
                })
        result_previews.append(previews)
        result_attachments.append(attachments)
    
    props['posts'] = results[0]
    response = make_response(render_template(
        'post.html',
        props = props,
        results = results,
        result_previews = result_previews,
        result_attachments = result_attachments
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/board')
def board():
    props = {
        'currentPage': 'board'
    }
    response = make_response(render_template(
        'board_list.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/requests')
def requests():
    props = {
        'currentPage': 'requests'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    if not request.args.get('commit'):
        query = "SELECT * FROM requests "
        query += "WHERE status = 'open' "
        query += "ORDER BY votes desc "
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params = (offset,)
        query += "LIMIT 25"
    else:
        query = "SELECT * FROM requests "
        query += "WHERE title ILIKE %s "
        params = ('%' + request.args.get('q') + '%',)
        if request.args.get('service'):
            query += "AND service = %s "
            params += (request.args.get('service'),)
        query += "AND service != 'discord' "
        if request.args.get('max_price'):
            query += "AND price <= %s "
            params += (request.args.get('max_price'),)
        query += "AND status = %s "
        params += (request.args.get('status'),)
        query += "ORDER BY " + {
            'votes': 'votes',
            'created': 'created',
            'price': 'price'
        }.get(request.args.get('sort_by'), 'votes')
        query += {
            'asc': ' asc ',
            'desc': ' desc '
        }.get(request.args.get('order'), 'desc')
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params += (offset,)
        query += "LIMIT 25"

    cursor = get_cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()

    response = make_response(render_template(
        'requests_list.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/requests/<id>/vote_up', methods=['POST'])
def vote_up(id):
    ip = request.args.get('CF-Connecting-IP') if request.args.get('CF-Connecting-IP') else request.remote_addr
    query = "SELECT * FROM requests WHERE id = %s"
    params = (id,)

    cursor = get_cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()

    props = {
        'currentPage': 'requests',
        'redirect': request.args.get('Referer') if request.args.get('Referer') else '/requests'
    }

    if not len(result):
        abort(404)
    hash = sha256(ip.encode()).hexdigest()
    if hash in result.get('ips'):
        props['message'] = 'You already voted on this request.'
        return make_response(render_template(
            'error.html',
            props = props
        ), 401)
    else:
        record = result.get('ips')
        record.append(hash)
        query = "UPDATE requests SET votes = votes + 1,"
        query += "ips = %s "
        params = (record,)
        query += "WHERE id = %s"
        params += (id,)
        cursor.execute(query, params)

        return make_response(render_template(
            'success.html',
            props = props
        ))

### API ###

@app.route('/api/bans')
def bans():
    cursor = get_cursor()
    query = "SELECT * FROM dnp"
    cursor.execute(query)
    results = cursor.fetchall()
    return make_response(jsonify(results), 200)

@app.route('/api/recent')
def recent():
    cursor = get_cursor()
    query = "SELECT * FROM booru_posts ORDER BY added desc "
    params = ()

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    response = make_response(jsonify(results), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/api/lookup')
def lookup():
    if (request.args.get('q') is None):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM lookup "
    params = ()
    query += "WHERE name ILIKE %s "
    params += ('%' + request.args.get('q') + '%',)
    if (request.args.get('service')):
        query += "AND service = %s "
        params += (request.args.get('service'),)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 50
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    response = make_response(jsonify(list(map(lambda x: x['id'], results))), 200)
    return response

# @app.route('/api/discord/channels/lookup')
# def discord_lookup():

@app.route('/api/lookup/cache/<id>')
def lookup_cache(id):
    if (request.args.get('service') is None):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM lookup WHERE id = %s AND service = %s"
    params = (id, request.args.get('service'))
    cursor.execute(query, params)
    results = cursor.fetchall()
    response = make_response(jsonify({ "name": results[0]['name'] if results[0]['name'] else '' }))
    return response