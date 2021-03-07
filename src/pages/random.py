from flask import Blueprint, redirect, url_for, g

from ..utils.utils import make_cache_key
from ..internals.cache.redis import get_conn
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor

from ..lib.artist import get_artist, get_non_discord_artist_keys
from ..lib.post import get_post, get_all_post_keys
from ..lib.ab_test import get_ab_variant
from ..utils.utils import get_value

import random as rand

random = Blueprint('random', __name__)

@random.route('/posts/random')
def random_post():
    variant = get_ab_variant('random_post_redis')

    post = None
    if variant == 'CONTROL':
        cursor = get_cursor()
        query = "SELECT service, \"user\", id FROM posts WHERE random() < 0.01 LIMIT 1"
        cursor.execute(query)
        random = cursor.fetchall()
        post = get_value(random, 0)
    else:
        post = get_random_post()

    if post is None:
        return redirect('back')
    response = redirect(url_for('legacy.post', service = post['service'], id = post['user'], post = post['id']))
    response.autocorrect_location_header = False
    return response

@random.route('/artists/random')
def random_artist():
    variant = get_ab_variant('random_artist_redis')

    artist = {}
    if variant == 'CONTROL':
        cursor = get_cursor()
        query = "SELECT id, service FROM lookup WHERE service != 'discord-channel' ORDER BY random() LIMIT 1"
        cursor.execute(query)
        random = cursor.fetchall()
        artist = random[0]
    else:
        artist = get_random_artist()

    if artist is None:
        return redirect('back')
    response = redirect(url_for('artists.artist', service = artist['service'], id = artist['id']))
    response.autocorrect_location_header = False
    return response

def get_random_post():
    post_keys = get_all_post_keys()
    if len(post_keys) == 0:
        return None
    return rand.choice(post_keys)

def get_random_artist():
    artists = get_non_discord_artist_keys()
    if len(artists) == 0:
        return None
    return rand.choice(artists)
