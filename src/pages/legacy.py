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
from python_resumable import UploaderFlask
from flask import Flask, jsonify, render_template, render_template_string, request, redirect, url_for, send_from_directory, make_response, g, abort, session, Blueprint
from werkzeug.utils import secure_filename
from slugify import slugify_filename
import requests
from markupsafe import Markup
from bleach.sanitizer import Cleaner
from hashlib import sha256

from ..internals.database.database import get_cursor
from ..internals.cache.flask_cache import cache
from ..lib.post import is_post_flagged
from ..utils.utils import make_cache_key, relative_time, delta_key, allowed_file, limit_int

legacy = Blueprint('legacy', __name__)

@legacy.route('/artists/updated')
@cache.cached(key_prefix=make_cache_key)
def updated_artists():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)
    offset = int(request.args.get('o') or 0)
    limit = 25

    props['limit'] = limit

    with get_cursor() as cursor:
        query = 'SELECT posts.user, service, max(added) FROM posts GROUP BY posts.user, service ORDER BY max(added) desc '
        params = ()
        query += "OFFSET %s "
        params += (offset,)
        query += "LIMIT 25"
        cursor.execute(query, params)
        post_results = cursor.fetchall()

    with get_cursor() as cursor:
        count_query = "SELECT posts.user, service, max(added) FROM posts GROUP BY posts.user, service"
        cursor.execute(count_query)
        props["count"] = len(cursor.fetchall())

    base = request.args.to_dict()
    base.pop('o', None)

    results = []
    for post in post_results:
        with get_cursor() as cursor:
            lookup_query = "SELECT * FROM lookup WHERE id = %s AND service = %s"
            lookup_params = (post['user'], post['service'])
            cursor.execute(lookup_query, lookup_params)
            user_result = cursor.fetchone()
            if not user_result:
                continue
            results.append({
                "id": post['user'],
                "name": user_result['name'],
                "service": post['service'],
                "updated": post['max']
            })
    response = make_response(render_template(
        'updated.html',
        base = base,
        props = props,
        results = results
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@legacy.route('/posts')
def posts():
    props = {
        'currentPage': 'posts'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    limit = limit_int(request.args.get('limit') or 25, 50)
    offset = int(request.args.get('o') or 0)

    props['limit'] = limit

    if not request.args.get('q'):
        query = "SELECT * FROM posts "
        params = ()

        query += "ORDER BY added desc "
        query += "OFFSET %s "
        params += (offset,)
        query += "LIMIT %s"
        params += (limit,)
    else:
        query = "SET LOCAL enable_indexscan = off; "
        query += "SELECT * FROM posts WHERE to_tsvector('english', content || ' ' || title) @@ websearch_to_tsquery(%s) "
        params = (request.args.get('q'),)

        query += "ORDER BY added desc "
        offset = request.args.get('o') if request.args.get('o') else 0
        query += "OFFSET %s "
        params += (offset,)
        limit = request.args.get('limit') if request.args.get('limit') and request.args.get('limit') <= 50 else 25
        query += "LIMIT %s"
        params += (limit,)
    
    with get_cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    with get_cursor() as cursor:
        count_query = "SELECT COUNT(*) FROM posts "
        count_params = ()
        if request.args.get('q'):
            count_query += "WHERE to_tsvector('english', content || ' ' || title) @@ websearch_to_tsquery(%s)"
            count_params += (request.args.get('q'),)
        cursor.execute(count_query, count_params)
        props["count"] = int(cursor.fetchall()[0]["count"])

    result_previews = []
    result_attachments = []
    result_flagged = []
    result_after_kitsune = []
    result_is_image = []
    for post in results:
        if post['added'] > datetime(2020, 12, 22, 0, 0, 0, 0):
            result_after_kitsune.append(True)
        else:
            result_after_kitsune.append(False)
        previews = []
        attachments = []
        if len(post['file']):
            if re.search("\.(gif|jpe?g|jpe|png|webp)$", post['file']['path'], re.IGNORECASE):
                result_is_image.append(True)
                previews.append({
                    'type': 'thumbnail',
                    'path': post['file']['path'].replace('https://kemono.party','')
                })
            else:
                result_is_image.append(False)
                attachments.append({
                    'path': post['file']['path'],
                    'name': post['file'].get('name')
                })
        else:
            result_is_image.append(False)
        
        if len(post['embed']):
            previews.append({
                'type': 'embed',
                'url': post['embed']['url'],
                'subject': post['embed']['subject'],
                'description': post['embed']['description']
            })
        for attachment in post['attachments']:
            if re.search("\.(gif|jpe?g|jpe|png|webp)$", attachment['path'], re.IGNORECASE):
                previews.append({
                    'type': 'thumbnail',
                    'path': attachment['path'].replace('https://kemono.party','')
                })
            else:
                attachments.append({
                    'path': attachment['path'],
                    'name': attachment['name']
                })
        
        result_flagged.append(is_post_flagged(post['service'], post['user'], post['id']))
        result_previews.append(previews)
        result_attachments.append(attachments)
    
    response = make_response(render_template(
        'posts.html',
        props = props,
        results = results,
        base = base,
        result_previews = result_previews,
        result_attachments = result_attachments,
        result_flagged = result_flagged,
        result_after_kitsune = result_after_kitsune,
        result_is_image = result_is_image
    ), 200)
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response

@legacy.route('/posts/upload')
def upload_post():
    props = {
        'currentPage': 'posts'
    }
    response = make_response(render_template(
        'upload.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

# TODO: /:service/user/:id/rss

@legacy.route('/<service>/user/<id>/rss')
def user_rss(service, id):
    with get_cursor() as cursor:
        query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s "
        params = (id, service)

        query += "ORDER BY added desc "
        query += "LIMIT 10"

        cursor.execute(query, params)
        results = cursor.fetchall()

    with get_cursor() as cursor:
        lookup_query = "SELECT * FROM lookup WHERE id = %s AND service = %s"
        lookup_params = (id, service)
        cursor.execute(lookup_query, lookup_params)
        results3 = cursor.fetchall()
        name = results3[0]['name'] if len(results3) > 0 else ''

    fg = FeedGenerator()
    fg.title(name)
    fg.description('Feed for posts from ' + name + '.')
    fg.id(f'http://{request.headers.get("host")}/{service}/user/{id}')
    fg.link(href=f'http://{request.headers.get("host")}/{service}/user/{id}')
    fg.generator(generator='Kemono')
    fg.ttl(ttl=40)

    for post in results:
        fe = fg.add_entry()
        fe.title(post['title'])
        fe.id(f'http://{request.headers.get("host")}/{service}/user/{id}/post/{post["id"]}')       
        fe.link(href=f'http://{request.headers.get("host")}/{service}/user/{id}/post/{post["id"]}')
        fe.content(content=post["content"])
        fe.pubDate(pytz.utc.localize(post["added"]))

    response = make_response(fg.atom_str(pretty=True), 200)
    response.headers['Content-Type'] = 'application/rss+xml'
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
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@legacy.route('/requests')
def requests_list():
    props = {
        'currentPage': 'requests'
    }
    base = request.args.to_dict()
    base.pop('o', None)
    props['limit'] = 25

    if not request.args.get('commit'):
        query = "SELECT * FROM requests "
        query += "WHERE status = 'open' "
        query += "ORDER BY votes desc "
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params = (offset,)
        query += "LIMIT 25"

        with get_cursor() as cursor:
            query2 = "SELECT COUNT(*) FROM requests "
            query2 += "WHERE status = 'open'"
            cursor.execute(query2)
            results2 = cursor.fetchall()
            props["count"] = int(results2[0]["count"])
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

        with get_cursor() as cursor:
            query2 = "SELECT COUNT(*) FROM requests "
            query2 += "WHERE title ILIKE %s "
            params2 = ('%' + request.args.get('q') + '%',)
            if request.args.get('service'):
                query2 += "AND service = %s "
                params2 += (request.args.get('service'),)
            query2 += "AND service != 'discord' "
            if request.args.get('max_price'):
                query2 += "AND price <= %s "
                params2 += (request.args.get('max_price'),)
            query2 += "AND status = %s"
            params2 += (request.args.get('status'),)
            cursor.execute(query2, params2)
            results2 = cursor.fetchall()
            props["count"] = int(results2[0]["count"])

    with get_cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    response = make_response(render_template(
        'requests_list.html',
        props = props,
        results = results,
        base = base
    ), 200)
    return response

@legacy.route('/requests/<id>/vote_up', methods=['POST'])
def vote_up(id):
    ip = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1] if 'X-Forwarded-For' in request.headers else request.remote_addr
    query = "SELECT * FROM requests WHERE id = %s"
    params = (id,)

    with get_cursor() as cursor:
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
        with get_cursor() as cursor:
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
        ), 200)

@legacy.route('/requests/new')
def request_form():
    props = {
        'currentPage': 'requests'
    }

    response = make_response(render_template(
        'requests_new.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@legacy.route('/requests/new', methods=['POST'])
def request_submit():
    props = {
        'currentPage': 'requests',
        'redirect': request.args.get('Referer') if request.args.get('Referer') else '/requests'
    }

    ip = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1] if 'X-Forwarded-For' in request.headers else request.remote_addr

    if not request.form.get('user_id'):
        props['message'] = 'You didn\'t enter a user ID.'
        return make_response(render_template(
            'error.html',
            props = props
        ), 400)

    if getenv('TELEGRAMTOKEN'):
        snippet = ''
        with open('views/requests_new.html', 'r') as file:
            snippet = file.read()

        requests.post(
            'https://api.telegram.org/bot' + getenv('TELEGRAMTOKEN') + '/sendMessage',
            params = {
                'chat_id': '-' + getenv('TELEGRAMCHANNEL'),
                'parse_mode': 'HTML',
                'text': render_template_string(snippet)
            }
        )

    filename = ''
    try:
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename and allowed_file(image.content_type, ['png', 'jpeg', 'gif']):
                filename = original = slugify_filename(secure_filename(image.filename))
                tmp = join('/tmp', filename)
                image.save(tmp)
                limit = int(getenv('REQUESTS_IMAGES')) if getenv('REQUESTS_IMAGES') else 1048576
                if stat(tmp).st_size > limit:
                    abort(413)
                try:
                    host = getenv('ARCHIVERHOST')
                    port = getenv('ARCHIVERPORT') if getenv('ARCHIVERPORT') else '8000'
                    r = requests.post(
                        f'http://{host}:{port}/api/upload/requests/images',
                        files = { 'file' : open(tmp, 'rb') }
                    )
                    filename = basename(r.text)
                    r.raise_for_status()
                except Exception:
                    return f'Error while connecting to archiver.', 500
    except Exception as error:
        props['message'] = 'Failed to upload image. Error: {}'.format(error)
        return make_response(render_template(
            'error.html',
            props = props
        ), 500)

    scrub = Cleaner(tags = [])
    text = Cleaner(tags = ['br'])

    columns = ['service','"user"','title','description','price','ips']
    description = request.form.get('description').strip().replace('\n', '<br>\n')
    params = (
        scrub.clean(request.form.get('service')),
        scrub.clean(request.form.get('user_id').strip()),
        scrub.clean(request.form.get('title').strip()),
        text.clean(description),
        scrub.clean(request.form.get('price').strip()),
        [sha256(ip.encode()).hexdigest()]
    )
    if request.form.get('specific_id'):
        columns.append('post_id')
        params += (scrub.clean(request.form.get('specific_id').strip()),)
    if filename:
        columns.append('image')
        params += (join('/requests', 'images', filename),)
    data = ['%s'] * len(params)

    query = "INSERT INTO requests ({fields}) VALUES ({values})".format(
        fields = ','.join(columns),
        values = ','.join(data)
    )

    with get_cursor() as cursor:
        cursor.execute(query, params)

    return make_response(render_template(
        'success.html',
        props = props
    ), 200)

@legacy.route('/api/upload', methods=['POST'])
def upload():
    resumable_dict = {
        'resumableIdentifier': request.form.get('resumableIdentifier'),
        'resumableFilename': request.form.get('resumableFilename'),
        'resumableTotalSize': request.form.get('resumableTotalSize'),
        'resumableTotalChunks': request.form.get('resumableTotalChunks'),
        'resumableChunkNumber': request.form.get('resumableChunkNumber')
    }

    if int(request.form.get('resumableTotalSize')) > int(getenv('UPLOAD_LIMIT')):
        return "File too large.", 415

    makedirs('/tmp/uploads', exist_ok=True)
    makedirs('/tmp/uploads/incomplete', exist_ok=True)

    resumable = UploaderFlask(
        resumable_dict,
        '/tmp/uploads',
        '/tmp/uploads/incomplete',
        request.files['file']
    )

    resumable.upload_chunk()

    if resumable.check_status() is True:
        resumable.assemble_chunks()
        try:
            resumable.cleanup()
        except:
            pass

        try:
            host = getenv('ARCHIVERHOST')
            port = getenv('ARCHIVERPORT') if getenv('ARCHIVERPORT') else '8000'
            r = requests.post(
                f'http://{host}:{port}/api/upload/uploads',
                files = { 'file' : open(join('/tmp/uploads', request.form.get('resumableFilename')), 'rb') }
            )
            final_path = r.text
            r.raise_for_status()
        except Exception:
            return f'Error while connecting to archiver.', 500

        post_model = {
            'id': ''.join(random.choice(string.ascii_letters) for x in range(8)),
            '"user"': request.form.get('user'),
            'service': request.form.get('service'),
            'title': request.form.get('title'),
            'content': request.form.get('content') or "",
            'embed': {},
            'shared_file': True,
            'added': datetime.now(),
            'published': datetime.now(),
            'edited': None,
            'file': {
                "name": basename(final_path),
                "path": final_path
            },
            'attachments': []
        }

        post_model['embed'] = json.dumps(post_model['embed'])
        post_model['file'] = json.dumps(post_model['file'])
        
        columns = post_model.keys()
        data = ['%s'] * len(post_model.values())
        data[-1] = '%s::jsonb[]' # attachments
        query = "INSERT INTO posts ({fields}) VALUES ({values})".format(
            fields = ','.join(columns),
            values = ','.join(data)
        )
        
        with get_cursor() as cursor:
            cursor.execute(query, list(post_model.values()))
        
        return jsonify({
            "fileUploadStatus": True,
            "resumableIdentifier": resumable.repo.file_id
        })

    return jsonify({
        "chunkUploadStatus": True,
        "resumableIdentifier": resumable.repo.file_id
    })

@legacy.route('/api/bans')
def bans():
    with get_cursor() as cursor:
        query = "SELECT * FROM dnp"
        cursor.execute(query)
        results = cursor.fetchall()
    return make_response(jsonify(results), 200)

@legacy.route('/api/recent')
def recent():
    with get_cursor() as cursor:
        query = "SELECT * FROM posts ORDER BY added desc "
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

@legacy.route('/api/lookup')
def lookup():
    if (request.args.get('q') is None):
        return make_response('Bad request', 400)
    
    with get_cursor() as cursor:
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
    with get_cursor() as cursor:
        query = "SELECT channel FROM discord_posts WHERE server = %s GROUP BY channel"
        params = (request.args.get('q'),)
        cursor.execute(query, params)
        channels = cursor.fetchall()
        lookup = []
        for x in channels:
            cursor.execute("SELECT * FROM lookup WHERE service = 'discord-channel' AND id = %s", (x['channel'],))
            lookup_result = cursor.fetchall()
            lookup.append({ 'id': x['channel'], 'name': lookup_result[0]['name'] if len(lookup_result) else '' })
    response = make_response(jsonify(lookup))
    return response

@legacy.route('/api/discord/channel/<id>')
def discord_channel(id):
    with get_cursor() as cursor:
        query = "SELECT * FROM discord_posts WHERE channel = %s ORDER BY published desc "
        params = (id,)

        offset = request.args.get('skip') if request.args.get('skip') else 0
        query += "OFFSET %s "
        params += (offset,)
        limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 25
        query += "LIMIT %s"
        params += (limit,)

        cursor.execute(query, params)
        results = cursor.fetchall()
    return jsonify(results)

@legacy.route('/api/lookup/cache/<id>')
def lookup_cache(id):
    if (request.args.get('service') is None):
        return make_response('Bad request', 400)
    with get_cursor() as cursor:
        query = "SELECT * FROM lookup WHERE id = %s AND service = %s"
        params = (id, request.args.get('service'))
        cursor.execute(query, params)
        results = cursor.fetchall()
    response = make_response(jsonify({ "name": results[0]['name'] if len(results) > 0 else '' }))
    return response

@legacy.route('/api/<service>/user/<user>/lookup')
def user_search(service, user):
    if (request.args.get('q') and len(request.args.get('q')) > 35):
        return make_response('Bad request', 400)
    with get_cursor() as cursor:
        query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s "
        params = (user, service)
        query += "AND to_tsvector(content || ' ' || title) @@ websearch_to_tsquery(%s) "
        params += (request.args.get('q'),)
        query += "ORDER BY published desc "

        offset = request.args.get('o') if request.args.get('o') else 0
        query += "OFFSET %s "
        params += (offset,)
        limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 25
        query += "LIMIT %s"
        params += (limit,)

        cursor.execute(query, params)
        results = cursor.fetchall()
    return jsonify(results)

@legacy.route('/api/<service>/user/<user>/post/<post>')
def post_api(service, user, post):
    with get_cursor() as cursor:
        query = "SELECT * FROM posts WHERE id = %s AND \"user\" = %s AND service = %s ORDER BY added asc"
        params = (post, user, service)
        cursor.execute(query, params)
        results = cursor.fetchall()
    return jsonify(results)

@legacy.route('/api/<service>/user/<user>/post/<post>/flag')
def flag_api(service, user, post):
    with get_cursor() as cursor:
        query = "SELECT * FROM booru_flags WHERE id = %s AND \"user\" = %s AND service = %s"
        params = (post, user, service)
        cursor.execute(query, params)
        results = cursor.fetchall()
    return "", 200 if len(results) else 404

@legacy.route('/api/<service>/user/<user>/post/<post>/flag', methods=["POST"])
def new_flag_api(service, user, post):
    with get_cursor() as cursor:
        query = "SELECT * FROM posts WHERE id = %s AND \"user\" = %s AND service = %s"
        params = (post, user, service)
        cursor.execute(query, params)
        results = cursor.fetchall()
        if len(results) == 0:
            return "", 404

    with get_cursor() as cursor:
        query2 = "SELECT * FROM booru_flags WHERE id = %s AND \"user\" = %s AND service = %s"
        params2 = (post, user, service)
        cursor.execute(query2, params2)
        results2 = cursor.fetchall()
        if len(results2) > 0:
            # conflict; flag already exists
            return "", 409

    scrub = Cleaner(tags = [])
    columns = ['id','"user"','service']
    params = (
        scrub.clean(post),
        scrub.clean(user),
        scrub.clean(service)
    )
    data = ['%s'] * len(params)
    query = "INSERT INTO booru_flags ({fields}) VALUES ({values})".format(
        fields = ','.join(columns),
        values = ','.join(data)
    )
    with get_cursor() as cursor:
        cursor.execute(query, params)

    return "", 200

@legacy.route('/api/<service>/user/<id>')
@cache.cached(key_prefix=make_cache_key)
def user_api(service, id):
    with get_cursor() as cursor:
        query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s ORDER BY published desc "
        params = (id, service)

        offset = request.args.get('o') if request.args.get('o') else 0
        query += "OFFSET %s "
        params += (offset,)
        limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 25
        query += "LIMIT %s"
        params += (limit,)

        cursor.execute(query, params)
        results = cursor.fetchall()

    return jsonify(results)