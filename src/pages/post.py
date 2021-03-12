from flask import Blueprint, request, make_response, render_template, redirect, url_for

import datetime
import re

from ..utils.utils import make_cache_key
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor
from ..lib.post import get_post, is_post_flagged, get_next_post_id, get_previous_post_id

post = Blueprint('post', __name__)

@post.route('/<service>/user/<user_id>/post/<post_id>/prev')
def post_prev(service, user_id, post_id):
    previous_post_id = get_previous_post_id(post_id, user_id, service)

    previous_post = None
    if previous_post_id is not None:
        previous_post = get_post(previous_post_id, user_id, service)

    if not previous_post:
        response = redirect(request.headers.get('Referer') if request.headers.get('Referer') else '/')
    else:
        response = redirect(url_for('post.get', service = previous_post['service'], user_id = previous_post['user'], post_id = previous_post['id']))
        response.autocorrect_location_header = False

    return response

@post.route('/<service>/user/<user_id>/post/<post_id>/next')
def post_next(service, user_id, post_id):
    next_post_id = get_next_post_id(post_id, user_id, service)
    
    next_post = None
    if next_post_id is not None:
        next_post = get_post(next_post_id, user_id, service)

    if not next_post:
        response = redirect(request.headers.get('Referer') if request.headers.get('Referer') else '/')
    else:
        response = redirect(url_for('post.get', service = next_post['service'], user_id = next_post['user'], post_id = next_post['id']))
        response.autocorrect_location_header = False

    return response

@post.route('/<service>/user/<user_id>/post/<post_id>')
def post(service, user_id, post_id):
    cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'service': service if service else 'patreon'
    }

    post = get_post(post_id, user_id, service)
    if post is None:
        return redirect(url_for('artists.get', service = service, id = user_id))

    result_previews = None
    result_attachments = None
    result_flagged = None
    result_after_kitsune = False

    if post['added'] > datetime.datetime(2020, 12, 22, 0, 0, 0, 0):
        result_after_kitsune = True
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

    result_flagged = is_post_flagged(post_id, user_id, service)
    result_previews = previews
    result_attachments = attachments
    
    response = make_response(render_template(
        'post.html',
        props = props,
        post = post,
        result_previews = result_previews,
        result_attachments = result_attachments,
        result_flagged = result_flagged,
        result_after_kitsune = result_after_kitsune
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response
