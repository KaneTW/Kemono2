from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..internals.cache.redis import get_conn

import ujson
import copy
import dateutil

def get_favorite_artists(account_id = None, reload = False):
    redis = get_conn()
    key = 'favorite_artists:' + str(account_id)
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = '''
            select aaf.*, l.indexed from account_artist_favorite aaf
            inner join lookup l on aaf.service = l.service and aaf.artist_id = p.user
            where aaf.account_id = %s
        '''
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_favorites(favorites))
    else:
        favorites = deserialize_favorites(favorites)

    return favorites

def get_favorite_posts(account_id = None, reload = False):
    redis = get_conn()
    key = 'favorite_posts:' + str(account_id)
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = '''
            select apf.*, p.published from account_post_favorite apf
            inner join posts p on apf.service = p.service and apf.post_id = p.id and apf.artist_id = p.user
            where apf.account_id = %s
        '''
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_favorites(favorites))
    else:
        favorites = serialize_favorites(favorites)

    return favorites

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

def serialize_favorites(favorites):
    return ujson.dumps(favorites)

def deserialize_favorites(favorites):
    return ujson.loads(favorites)
