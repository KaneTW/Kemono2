import re
import random
import string
import json
import pytz
from feedgen.feed import FeedGenerator
from urllib.parse import urlencode
from datetime import datetime, timedelta
from os import getenv, stat, rename, makedirs
from os.path import join, dirname, isfile, splitext, basename
from shutil import move

from PIL import Image
from decimal import Decimal
from python_resumable import UploaderFlask
from flask import Flask, jsonify, render_template, render_template_string, request, redirect, url_for, send_from_directory, make_response, g, abort, session, Blueprint, flash
from werkzeug.utils import secure_filename
from slugify import slugify_filename
import requests
from markupsafe import Markup
from bleach.sanitizer import Cleaner
from hashlib import sha256

from src.config import Configuration
from ..lib.account import load_account
from ..internals.database.database import get_cursor
from ..internals.cache.flask_cache import cache
from ..utils.utils import make_cache_key, relative_time, delta_key, allowed_file, limit_int

legacy = Blueprint('legacy', __name__)


@legacy.route('/posts/upload')
def upload_post():
    account = load_account()
    if Configuration().filehaus['requires_account'] and account is None:
        flash('Filehaus uploading requires an account.')
        return redirect(url_for('account.get_login'))
    required_roles = Configuration().filehaus['required_roles']
    if len(required_roles) and account['role'] not in required_roles:
        flash(
            'Filehaus uploading requires elevated permissions. '
            'Please contact the administrator to change your role.'
        )
        return redirect(url_for('account.get_account'))
    props = {
        'currentPage': 'posts'
    }
    response = make_response(render_template(
        'upload.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response


@legacy.route('/discord/server/<id>')
def discord_server(id):
    response = make_response(render_template(
        'discord.html'
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response


@legacy.route('/board')
def board():
    props = {
        'currentPage': 'board'
    }
    response = make_response(render_template(
        'board_list.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response


@legacy.route('/api/upload', methods=['POST'])
def upload():
    account = load_account()
    if not account or account['role'] not in ['administrator', 'moderator', 'uploader']:
        return abort(403)

    service = request.form.get('service', None)
    user = request.form.get('user', None)
    uploads = json.loads(request.form['uppyResult'])
    model = dict(
        name=request.form.get('title'),
        description=request.form.get('content', ''),
        uploader=session.get('account_id')
    )
    query = """
        INSERT INTO shares ({fields})
        VALUES ({values})
        RETURNING *
    """.format(
        fields=','.join(model.keys()),
        values=','.join(['%s'] * len(model.values()))
    )
    cursor = get_cursor()
    cursor.execute(query, list(model.values()))
    returned = cursor.fetchone()
    share_id = returned['id']
    for upload in uploads:
        for u in upload['successful']:
            file_rel = dict(
                upload_id=u['tus']['uploadUrl'].split('/files/')[-1],
                upload_url=u['tus']['uploadUrl'],
                filename=u['name'],
                share_id=share_id
            )
            get_cursor().execute("""
                INSERT INTO file_share_relationships ({fields})
                VALUES ({values})
            """.format(
                fields=','.join(file_rel.keys()),
                values=','.join(['%s'] * len(file_rel.values()))
            ), list(file_rel.values()))

            lookup_rel = dict(
                share_id=share_id,
                service=service,
                user_id=user
            )
            get_cursor().execute("""
                INSERT INTO lookup_share_relationships ({fields})
                VALUES ({values})
            """.format(
                fields=','.join(lookup_rel.keys()),
                values=','.join(['%s'] * len(lookup_rel.values()))
            ), list(lookup_rel.values()))

    # This should redirect to the share
    return '', 200


@legacy.route('/api/creators')
def creators():
    cursor = get_cursor()
    query = """
        SELECT
            l.id,
            l.name,
            l.service,
            extract(epoch from l.indexed) AS indexed,
            extract(epoch from l.updated) AS updated,
            coalesce(aaf.favorited, 0) AS favorited
        FROM lookup l
        LEFT JOIN (
            SELECT
                artist_id,
                service,
                count(*) AS favorited
            FROM account_artist_favorite
            WHERE service != 'discord-channel'
            GROUP BY artist_id, service
        ) aaf ON
            l.id = aaf.artist_id
            AND l.service = aaf.service
        WHERE
            l.service != 'discord-channel'
            AND l.id NOT IN (SELECT id from dnp);
    """
    cursor.execute(query)
    results = cursor.fetchall()
    # Handle decimals.
    for result in results:
        for key in result.keys():
            if isinstance(result[key], Decimal):
                result[key] = float(result[key])
    return make_response(jsonify(results), 200)


@legacy.route('/api/bans')
def bans():
    cursor = get_cursor()
    query = "SELECT * FROM dnp"
    cursor.execute(query)
    results = cursor.fetchall()
    return make_response(jsonify(results), 200)


@legacy.route('/api/recent')
def recent():
    cursor = get_cursor()
    query = "SELECT * FROM posts ORDER BY added desc "
    params = ()

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 50
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    response = make_response(jsonify(results), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response


@legacy.route('/api/lookup')
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


@legacy.route('/api/discord/channels/lookup')
def discord_lookup():
    cursor = get_cursor()
    query = "SELECT channel FROM discord_posts WHERE server = %s GROUP BY channel"
    params = (request.args.get('q'),)
    cursor.execute(query, params)
    channels = cursor.fetchall()
    lookup = []
    for x in channels:
        cursor = get_cursor()
        cursor.execute("SELECT * FROM lookup WHERE service = 'discord-channel' AND id = %s", (x['channel'],))
        lookup_result = cursor.fetchall()
        lookup.append({'id': x['channel'], 'name': lookup_result[0]['name'] if len(lookup_result) else ''})
    response = make_response(jsonify(lookup))
    return response


@legacy.route('/api/discord/channel/<id>')
def discord_channel(id):
    cursor = get_cursor()
    query = "SELECT * FROM discord_posts WHERE channel = %s ORDER BY published desc "
    params = (id,)

    offset = request.args.get('skip') if request.args.get('skip') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 50
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    return jsonify(results)


@legacy.route('/api/lookup/cache/<id>')
def lookup_cache(id):
    if (request.args.get('service') is None):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM lookup WHERE id = %s AND service = %s"
    params = (id, request.args.get('service'))
    cursor.execute(query, params)
    results = cursor.fetchall()
    response = make_response(jsonify({"name": results[0]['name'] if len(results) > 0 else ''}))
    return response


@legacy.route('/api/<service>/user/<user>/lookup')
def user_search(service, user):
    if (request.args.get('q') and len(request.args.get('q')) > 35):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s "
    params = (user, service)
    query += "AND to_tsvector(content || ' ' || title) @@ websearch_to_tsquery(%s) "
    params += (request.args.get('q'),)
    query += "ORDER BY published desc "

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 50
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    return jsonify(results)


@legacy.route('/api/<service>/user/<user>/post/<post>')
def post_api(service, user, post):
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE id = %s AND \"user\" = %s AND service = %s ORDER BY added asc"
    params = (post, user, service)
    cursor.execute(query, params)
    results = cursor.fetchall()
    return jsonify(results)


@legacy.route('/api/<service>/user/<user>/post/<post>/flag')
def flag_api(service, user, post):
    cursor = get_cursor()
    query = "SELECT * FROM booru_flags WHERE id = %s AND \"user\" = %s AND service = %s"
    params = (post, user, service)
    cursor.execute(query, params)
    results = cursor.fetchall()
    return "", 200 if len(results) else 404


@legacy.route('/api/<service>/user/<user>/post/<post>/flag', methods=["POST"])
def new_flag_api(service, user, post):
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE id = %s AND \"user\" = %s AND service = %s"
    params = (post, user, service)
    cursor.execute(query, params)
    results = cursor.fetchall()
    if len(results) == 0:
        return "", 404

    cursor2 = get_cursor()
    query2 = "SELECT * FROM booru_flags WHERE id = %s AND \"user\" = %s AND service = %s"
    params2 = (post, user, service)
    cursor2.execute(query2, params2)
    results2 = cursor.fetchall()
    if len(results2) > 0:
        # conflict; flag already exists
        return "", 409

    scrub = Cleaner(tags=[])
    columns = ['id', '"user"', 'service']
    params = (
        scrub.clean(post),
        scrub.clean(user),
        scrub.clean(service)
    )
    data = ['%s'] * len(params)
    query = "INSERT INTO booru_flags ({fields}) VALUES ({values})".format(
        fields=','.join(columns),
        values=','.join(data)
    )
    cursor3 = get_cursor()
    cursor3.execute(query, params)

    return "", 200


@legacy.route('/api/<service>/user/<id>')
@cache.cached(key_prefix=make_cache_key)
def user_api(service, id):
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s ORDER BY published desc "
    params = (id, service)

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 50
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    return jsonify(results)
