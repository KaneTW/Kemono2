from flask import Blueprint, request, make_response, render_template, redirect, url_for
from pathlib import PurePath
from bleach.sanitizer import Cleaner
import datetime
import re

from ..utils.utils import make_cache_key
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor
from ..lib.post import get_post, is_post_flagged, get_next_post_id, get_previous_post_id, get_post_comments
from ..lib.artist import get_artist
from ..lib.favorites import is_post_favorited
from ..lib.account import load_account

post = Blueprint('post', __name__)
video_extensions = ['.mp4', '.webm']


@post.route('/<service>/user/<artist_id>/post/<post_id>')
def get(service, artist_id, post_id):
    # cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'service': service if service else 'patreon'
    }

    post = get_post(post_id, artist_id, service)
    if post is None:
        response = redirect(url_for('artists.get', service=service, artist_id=artist_id))
        return response

    comments = get_post_comments(post_id, service)

    favorited = False
    account = load_account()
    if account is not None:
        favorited = is_post_favorited(account['id'], service, artist_id, post_id)

    artist = get_artist(service, artist_id)

    previews = []
    attachments = []
    videos = []
    if len(post['file']):
        if re.search("\.(gif|jpe?g|jpe|png|webp)$", post['file']['path'], re.IGNORECASE):  # noqa w605
            previews.append({
                'type': 'thumbnail',
                'name': post['file'].get('name'),
                'path': post['file']['path'].replace('https://kemono.party', '')
            })
        else:
            path = post['file']['path'].replace('https://kemono.party', '')
            file_extension = PurePath(path).suffix
            # filename without extension
            stem = PurePath(path).stem
            attachments.append({
                'path': path,
                'name': post['file'].get('name'),
                'extension': file_extension,
                'stem': stem
            })
    if len(post['embed']):
        previews.append({
            'type': 'embed',
            'url': post['embed']['url'],
            'subject': post['embed']['subject'],
            'description': post['embed']['description']
        })
    for attachment in post['attachments']:
        if re.search("\.(gif|jpe?g|jpe|png|webp)$", attachment['path'], re.IGNORECASE):  # noqa w605
            previews.append({
                'type': 'thumbnail',
                'name': attachment['name'],
                'path': attachment['path'].replace('https://kemono.party', '')
            })
        else:
            file_extension = PurePath(attachment['path']).suffix
            # filename without extension
            stem = PurePath(attachment['path']).stem
            attachments.append({
                'path': attachment['path'],
                'name': attachment.get('name'),
                'extension': file_extension,
                'stem': stem
            })
    for attachment in attachments:
        if attachment['extension'] in video_extensions:
            videos.append({
                'path': attachment['path'],
                'name': attachment.get('name'),
                'extension': attachment['extension']
            })
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
        'i', 'li', 'ol', 'strong', 'ul', 'img', 'br', 'h1',
        'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span',
        'ul', 'ol', 'li'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'acronym': ['title'],
        'abbr': ['title'],
        'img': ['src'],
    }
    if post['service'] == 'fanbox':
        # Some Fanbox embeds require the usage of IFrame
        allowed_tags += ['iframe']
        allowed_attributes['iframe'] = ['src']
    scrub = Cleaner(
        attributes=allowed_attributes,
        tags=allowed_tags,
        strip=True
    )
    post['content'] = scrub.clean(post['content'])

    props['artist'] = artist
    props['flagged'] = is_post_flagged(service, artist_id, post_id)
    props['favorited'] = favorited
    props['after_kitsune'] = post['added'] > datetime.datetime(2020, 12, 22, 0, 0, 0, 0)
    response = make_response(render_template(
        'post.html',
        props=props,
        post=post,
        comments=comments,
        result_previews=previews,
        result_attachments=attachments,
        videos=videos,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response
