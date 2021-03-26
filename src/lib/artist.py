from ..internals.cache.redis import get_conn
from ..internals.database.database import get_cursor
import ujson
import dateutil
import copy

def get_non_discord_artist_keys(reload = False):
    redis = get_conn()
    key = 'non_discord_artist_keys'
    artist_keys = redis.get(key)
    if artist_keys is None or reload:
        cursor = get_cursor()
        query = "SELECT id, service FROM lookup WHERE service != 'discord-channel'"
        cursor.execute(query)
        artist_keys = cursor.fetchall()
        redis.set(key, ujson.dumps(artist_keys), ex = 600)
    else:
        artist_keys = ujson.loads(artist_keys)
    return artist_keys

def get_all_non_discord_artists(reload = False):
    redis = get_conn()
    key = 'non_discord_artists'
    artists = redis.get(key)
    if artists is None or reload:
        cursor = get_cursor()
        query = "SELECT * FROM lookup WHERE service != 'discord-channel'"
        cursor.execute(query)
        artists = cursor.fetchall()
        redis.set(key, serialize_artists(artists), ex = 600)
    else:
        artists = deserialize_artists(artists)
    return artists

def get_artists_by_service(service, reload = False):
    redis = get_conn()
    key = 'artists_by_service:' + service
    artists = redis.get(key)
    if artists is None or reload:
        cursor = get_cursor()
        query = "SELECT * FROM lookup WHERE service = %s"
        cursor.execute(query, (service,))
        artists = cursor.fetchall()
        redis.set(key, serialize_artists(artists), ex = 600)
    else:
        artists = deserialize_artists(artists)
    return artists

def get_artist(service, artist_id, reload = False):
    redis = get_conn()
    key = 'artist:' + service + ':' + str(artist_id)
    artist = redis.get(key)
    if artist is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM lookup WHERE id = %s AND service = %s'
        cursor.execute(query, (artist_id, service,))
        artist = cursor.fetchone()
        redis.set(key, serialize_artist(artist), ex = 600)
    else:
        artist = deserialize_artist(artist)
    return artist

def get_artist_post_count(service, artist_id, reload = False):
    redis = get_conn()
    key = 'artist_post_count:' + service + ':' + str(artist_id)
    count = redis.get(key)
    if count is None or reload:
        cursor = get_cursor()
        query = 'SELECT count(*) as count FROM posts WHERE \"user\" = %s'
        cursor.execute(query, (artist_id,))
        count = cursor.fetchone()['count']
        redis.set(key, str(count), ex = 600)
    else:
        count = int(count)
    return count

def serialize_artists(artists):
    artists = copy.deepcopy(artists)
    return ujson.dumps(list(map(lambda artist: prepare_artist_fields(artist), artists)))

def deserialize_artists(artists_str):
    artists = ujson.loads(artists_str)
    return list(map(lambda artist: rebuild_artist_fields(artist), artists))

def serialize_artist(artist):
    if artist is not None:
        artist = prepare_artist_fields(copy.deepcopy(artist))
    return ujson.dumps(artist)

def deserialize_artist(artist_str):
    artist = ujson.loads(artist_str)
    if artist is not None:
        artist = rebuild_artist_fields(artist)
    return artist

def prepare_artist_fields(artist):
    artist['indexed'] = artist['indexed'].isoformat()
    return artist

def rebuild_artist_fields(artist):
    artist['indexed'] = dateutil.parser.parse(artist['indexed'])
    return artist
