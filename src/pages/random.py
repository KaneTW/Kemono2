from flask import Blueprint, redirect, url_for

from ..utils.utils import make_cache_key
from ..internals.cache.redis import get_conn
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor
from ..lib.artist import get_artist, get_non_discord_artist_ids
from ..lib.post import get_post, get_all_post_ids
import random as rand

random = Blueprint('random', __name__)

@random.route('/posts/random')
def random_post():
    post = get_random_post()
    if post is None:
        return redirect('back')
    response = redirect(url_for('legacy.post', service = post['service'], id = post['user'], post = post['id']))
    response.autocorrect_location_header = False
    return response

@random.route('/artists/random')
def random_artist():
    artist = get_random_artist()
    if artist is None:
        return redirect('back')
    response = redirect(url_for('legacy.user', service = artist['service'], id = artist['id']))
    response.autocorrect_location_header = False
    return response

def get_random_post():
    post_ids = get_all_post_ids()
    if len(post_ids) == 0:
        return None
    post_id = rand.choice(post_ids)
    return get_post(post_id)

def get_random_artist():
    artist_ids = get_non_discord_artist_ids()
    if len(artist_ids) == 0:
        return None
    artist_id = rand.choice(artist_ids)
    return get_artist(artist_id)
