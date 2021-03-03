from ..internals.cache.redis import get_conn
from ..internals.database.database import get_cursor
import ujson

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
        redis.set(key, ujson.dumps(post_ids))
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
        redis.set(key, ujson.dumps(serialize_post(post)))
    else:
        post = deserialize_post(ujson.loads(post))
    return post

def serialize_post(post):
    post['added'] = post['added'].isoformat()
    post['published'] = post['published'].isoformat()
    post['edited'] = post['edited'].isoformat()
    return ujson.dumps(post)

def deserialize_post(post):
    post['added'] = dateutil.parser.parse(post['added'])
    post['published'] = dateutil.parser.parse(post['published'])
    post['edited'] = dateutil.parser.parse(post['edited'])
    return post
