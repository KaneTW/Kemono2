from ..internals.cache.redis import get_conn, deserialize_dict_list, serialize_dict_list
from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..types.kemono import User
import ujson
import dateutil
import copy
import datetime


def count_all_posts(reload=False):
    redis = get_conn()
    key = 'global_post_count'
    count = redis.get(key)
    if count is None or reload:
        cursor = get_cursor()
        query = 'SELECT COUNT(*) FROM posts'
        cursor.execute(query)
        count = cursor.fetchone()
        redis.set(key, str(count['count']), ex=600)
    else:
        count = int(count)
    return count


def get_all_posts(offset: int, reload=False):
    redis = get_conn()
    key = 'all_posts:' + str(offset)
    all_posts = redis.get(key)
    if all_posts is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM posts OFFSET %s LIMIT 25'
        cursor.execute(query, (offset,))
        all_posts = cursor.fetchall()
        redis.set(key, serialize_dict_list(all_posts), ex=600)
    else:
        all_posts = deserialize_dict_list(all_posts)
    return all_posts


def get_all_posts_for_query(q: str, reload=False):
    redis = get_conn()
    key = 'all_posts_for_query:' + q
    results = redis.get(key)
    if results is None or reload:
        cursor = get_cursor()
        query = "SET LOCAL enable_indexscan = off; "
        query += "SELECT * FROM posts WHERE to_tsvector('english', content || ' ' || title) @@ websearch_to_tsquery(%s) ORDER BY added desc"
        params = (q,)

        cursor.execute(query, params)
        results = cursor.fetchall()
        redis.set(key, serialize_dict_list(results), ex=600)
    else:
        results = deserialize_dict_list(results)
    return results
