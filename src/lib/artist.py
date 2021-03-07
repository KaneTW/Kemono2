from ..internals.cache.redis import get_conn
from ..internals.database.database import get_cursor
import ujson
import dateutil
import copy

def get_non_discord_artist_ids(reload = False):
    redis = get_conn()
    key = 'non_discord_artist_ids'
    artist_ids = redis.get(key)
    if artist_ids is None or reload:
        cursor = get_cursor()
        query = "SELECT id FROM lookup WHERE service != 'discord-channel'"
        cursor.execute(query)
        artist_ids = cursor.fetchall()
        artist_ids = list(map(lambda row: row['id'], artist_ids))
        redis.set(key, ujson.dumps(artist_ids), ex = 600)
    else:
        artist_ids = ujson.loads(artist_ids)
    return artist_ids

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

def get_artist(artist_id, reload = False):
    redis = get_conn()
    key = 'artist:' + str(artist_id)
    artist = redis.get(key)
    if artist is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM lookup WHERE id = %s'
        cursor.execute(query, (artist_id,))
        artist = cursor.fetchone()
        redis.set(key, serialize_artist(artist), ex = 600)
    else:
        artist = deserialize_artist(artist)
    return artist

def get_artist_post_count(artist_id, reload = False):
    redis = get_conn()
    key = 'artist_post_count:' + str(artist_id)
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
    artist = prepare_artist_fields(copy.deepcopy(artist))
    return ujson.dumps(artist)

def deserialize_artist(artist_str):
    artist = ujson.loads(artist_str)
    artist = rebuild_artist_fields(artist)
    return artist

def prepare_artist_fields(artist):
    artist['indexed'] = artist['indexed'].isoformat()
    return artist

def rebuild_artist_fields(artist):
    artist['indexed'] = dateutil.parser.parse(artist['indexed'])
    return artist
