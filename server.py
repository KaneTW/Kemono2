from datetime import timedelta
from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))
from flask import Flask, render_template, request, redirect, g, abort, session

import src.internals.database.database as database
import src.internals.cache.redis as redis
from src.internals.cache.flask_cache import cache

from src.home import home
from src.legacy import legacy

app = Flask(
    __name__,
    template_folder='views'
)
app.register_blueprint(home)
app.register_blueprint(legacy)

app.config.from_pyfile('flask.cfg')
app.url_map.strict_slashes = False
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.search(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)

cache.init_app(app)

@app.before_request
def do_init_stuff():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=9999)
    session.modified = False

    app.config['DATABASE_POOL'] = database.make_pool()
    app.config['REDIS_POOL'] = redis.make_pool()
    
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        response = redirect(rp[:-1])
        response.autocorrect_location_header = False
        return response

@app.errorhandler(413)
def upload_exceeded(error):
    props = {
        'redirect': request.headers.get('Referer') if request.headers.get('Referer') else '/'
    }
    limit = int(getenv('REQUESTS_IMAGES')) if getenv('REQUESTS_IMAGES') else 1048576
    props['message'] = 'Submitted file exceeds the upload limit. {} MB for requests images.'.format(
        limit / 1024 / 1024
    )
    return render_template(
        'error.html',
        props = props
    ), 413

@app.teardown_appcontext
def close(e):
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()
        connection = g.pop('connection', None)
        if connection is not None:
            pool = database.get_pool()
            connection.commit()
            pool.putconn(connection)
