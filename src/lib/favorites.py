from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..internals.cache.redis import get_conn, serialize_dict_list, deserialize_dict_list
from ..lib.artist import get_artist
from ..lib.post import get_post

import ujson
import copy
import dateutil

def get_favorite_artists(account_id, reload = False):
    redis = get_conn()
    key = 'favorite_artists:' + str(account_id)
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = "select service, artist_id from account_artist_favorite where account_id"
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_dict_list(favorites))
    else:
        favorites = deserialize_dict_list(favorites)

    artists = []
    for favorite in favorites:
        artist = get_artist(favorite['service'], favorite['artist_id'])
        if artist is not None:
            artists.append(artist)
    return artists

def get_favorite_posts(account_id, reload = False):
    redis = get_conn()
    key = 'favorite_posts:' + str(account_id)
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = "select service, artist_id, post_id from account_post_favorite where account_id = %s"
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_dict_list(favorites))
    else:
        favorites = deserialize_dict_list(favorites)

    posts = []
    for favorite in favorites:
        post = get_post(favorite['post_id'], favorite['artist_id'], favorite['service'])
        if post is not None:
            posts.append(post)
    return posts

def add_favorite_artist(account_id, service, artist_id):
    cursor = get_cursor()
    query = 'insert into account_artist_favorite (account_id, service, artist_id) values (%s, %s, %s)'
    cursor.execute(query, (account_id, service, artist_id,))
    get_favorite_artists(account_id, True)

def add_favorite_post(account_id, service, artist_id, post_id):
    cursor = get_cursor()
    query = 'insert into account_post_favorite (account_id, service, artist_id, post_id) values (%s, %s, %s, %s)'
    cursor.execute(query, (account_id, service, artist_id, post_id))
    get_favorite_posts(account_id, True)
