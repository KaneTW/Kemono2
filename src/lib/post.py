from ..internals.cache.redis import get_conn
from ..internals.database.database import get_cursor
import ujson
import dateutil

def get_all_post_ids(reload = False):
    redis = get_conn()
    key = 'post_ids'
    post_ids = redis.get(key)
    if post_ids is None or reload:
        cursor = get_cursor()
        query = "SELECT id FROM posts"
        cursor.execute(query)
        post_ids = cursor.fetchall()
        post_ids = list(map(lambda row: row['id'], post_ids))
        redis.set(key, ujson.dumps(post_ids), ex = 600)
    else:
        post_ids = ujson.loads(post_ids)
    return post_ids

def get_post(post_id, reload = False):
    redis = get_conn()
    key = 'post:' + str(post_id)
    post = redis.get(key)
    if post is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM posts WHERE id = %s'
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()
        redis.set(key, serialize_post(post), ex = 600)
    else:
        post = deserialize_post(post)
    return post

def get_all_posts_by_artist(artist_id, reload = False):
    redis = get_conn()
    key = 'posts_by_artist:' + str(artist_id)
    posts = redis.get(key)
    if post is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM posts WHERE user = %s'
        cursor.execute(query, (artist_id,))
        posts = cursor.fetchone()
        redis.set(key, serialize_posts(posts), ex = 600)
    else:
        post = deserialize_posts(posts)
    return post

def get_artist_posts_with_offset_and_limit(artist_id, offset, reload = False):
    redis = get_conn()
    key = 'artist_posts_offset:' + str(artist_id) + ':' + str(offset)
    posts = redis.get(key)
    if post is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM posts WHERE id = %s OFFSET %s'
        cursor.execute(query, (artist_id, offset,))
        posts = cursor.fetchone()
        redis.set(key, serialize_posts(posts), ex = 600)
    else:
        post = deserialize_posts(posts)
    return post

def get_artist_post_with_search(id, search, offset, reload = False):
    redis = get_conn()
    key = 'artist_posts_offset:' + str(artist_id) + ':' + str(offset)
    posts = redis.get(key)
    if post is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM posts WHERE id = %s'
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()
        redis.set(key, serialize_post(post), ex = 600)
    else:
        post = deserialize_post(post)
    return post

def serialize_posts(posts):
    return ujson.dumps(list(map(lambda post: prepare_post_fields(post), posts)))

def deserialize_posts(posts_str):
    posts = ujson.loads(posts_str):
    return list(map(lambda post: rebuild_post_fields(post), posts))

def serialize_post(post):
    post = prepare_post_fields(post)
    return ujson.dumps(post)

def deserialize_post(post_str):
    post = ujson.loads(post_str)
    return rebuild_post_fields(post)    

def prepare_post_fields(post):
    post['added'] = post['added'].isoformat()
    post['published'] = post['published'].isoformat()
    post['edited'] = post['edited'].isoformat()
    return post

def rebuild_post_fields(post):
    post['added'] = dateutil.parser.parse(post['added'])
    post['published'] = dateutil.parser.parse(post['published'])
    post['edited'] = dateutil.parser.parse(post['edited'])
    return post
