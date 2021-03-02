import re
import random
import string
import json
import pytz
from feedgen.feed import FeedGenerator
from urllib.parse import urlencode
from datetime import datetime, timedelta
from os import getenv, stat, rename, makedirs
from os.path import join, dirname, isfile, splitext
from shutil import move
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

from PIL import Image
from python_resumable import UploaderFlask
from flask import Flask, jsonify, render_template, render_template_string, request, redirect, url_for, send_from_directory, make_response, g, abort, current_app, send_file, session
from flask_caching import Cache
from werkzeug.utils import secure_filename
from slugify import slugify_filename
import requests
from markupsafe import Markup
from bleach.sanitizer import Cleaner
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from hashlib import sha256

from src.internals.database.database import make_pool

from src.home import Home
from src.server import old_app

app = Flask(
    __name__,
    template_folder='views'
)
app.register_blueprint(Home)
app.register_blueprint(old_app)

app.config.from_pyfile('flask.cfg')
app.url_map.strict_slashes = False
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.search(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)

@app.before_request
def do_init_stuff():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(days=9999)
    session.modified = False

    app.config['DATABASE_POOL'] = make_pool()
    
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
            connection.commit()
            pool.putconn(connection)
