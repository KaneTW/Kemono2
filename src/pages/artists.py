from flask import Blueprint, request, make_response, render_template, session, redirect, url_for

import datetime
import re

from ..utils.utils import sort_dict_list_by, offset, take, limit_int
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor
from ..lib.artist import get_all_non_discord_artists, get_artist, get_artist_post_count, get_artists_by_service
from ..lib.post import get_artist_posts, get_all_posts_by_artist, is_post_flagged

artists = Blueprint('artists', __name__)

@artists.route('/artists')
def list():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    q = request.args.get('q')
    commit = request.args.get('commit')
    service = request.args.get('service')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order')
    offset = request.args.get('o') or 0
    limit = 25

    (results, total_count) = ([], 0)
    if commit is not None:
        (results, total_count) = get_artist_search_results(q, service, sort_by, order, offset, limit)

    props['count'] = total_count
    props['limit'] = limit

    response = make_response(render_template(
        'artists.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@artists.route('/<service>/user/<id>')
def user(service, id):
    cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'id': id,
        'service': service,
        'session': session
    }
    base = request.args.to_dict()
    base.pop('o', None)
    base["service"] = service
    base["id"] = id

    offset = int(request.args.get('o') or 0)
    query = request.args.get('q')
    limit = limit_int(int(request.args.get('limit') or 25), 50)

    (posts, total_count) = ([], 0)
    if query is None:
        (posts, total_count) = get_artist_post_page(id, service, offset, limit)
    else:
        (posts, total_count) = do_artist_post_search(id, service, query, offset, limit)

    artist = get_artist(id, service)
    if artist is None:
        return redirect(url_for('artists.list'))

    props['name'] = artist['name']
    props['count'] = total_count
    props['limit'] = limit

    result_previews = []
    result_attachments = []
    result_flagged = []
    result_after_kitsune = []
    for post in posts:
        if post['added'] > datetime.datetime(2020, 12, 22, 0, 0, 0, 0):
            result_after_kitsune.append(True)
        else:
            result_after_kitsune.append(False)
        previews = []
        attachments = []
        if len(post['file']):
            if re.search("\.(gif|jpe?g|jpe|png|webp)$", post['file']['path'], re.IGNORECASE):
                previews.append({
                    'type': 'thumbnail',
                    'path': post['file']['path'].replace('https://kemono.party','')
                })
            else:
                attachments.append({
                    'path': post['file']['path'],
                    'name': post['file'].get('name')
                })
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

        result_flagged.append(is_post_flagged(post['id'], post['user'], post['service']))
        result_previews.append(previews)
        result_attachments.append(attachments)
    
    response = make_response(render_template(
        'user.html',
        props = props,
        results = posts,
        base = base,
        result_previews = result_previews,
        result_attachments = result_attachments,
        result_flagged = result_flagged,
        result_after_kitsune = result_after_kitsune,
        session = session
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

def get_artist_search_results(q, service, sort_by, order, o, limit):
    if service:
        artists = get_artists_by_service(service)
    else:
        artists = get_all_non_discord_artists()

    page = []
    matches = []
    for artist in artists:
        if q in artist['name'].lower():
            matches.append(artist)

    matches = sort_dict_list_by(matches, sort_by, order=='desc')

    return (take(limit, offset(0, matches)), len(matches))

def do_artist_post_search(id, service, search, o, limit):
    posts = get_all_posts_by_artist(id, service)

    matches = []
    for post in posts:
        if search in post['content'].lower() or search in post['title'].lower():
            matches.append(post)

    matches = sort_dict_list_by(matches, 'published', True)

    return (take(limit, offset(o, matches)), len(matches))

def get_artist_post_page(artist_id, service, offset, limit):
    posts = get_artist_posts(artist_id, service, offset, limit, 'published desc')
    total_count = get_artist_post_count(artist_id)
    return (posts, total_count)
