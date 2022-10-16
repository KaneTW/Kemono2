from ..internals.cache.redis import get_conn, deserialize_dict_list, serialize_dict_list, KemonoRedisLock
from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..types.kemono import User
import ujson
import dateutil
import copy
import datetime
import redis_lock
import time


def count_all_posts(reload=False):
    redis = get_conn()
    key = 'global_post_count'
    count = redis.get(key)
    if count is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if lock.acquire(blocking=False):
            cursor = get_cursor()
            query = 'SELECT COUNT(*) FROM posts'
            cursor.execute(query)
            count = cursor.fetchone()
            redis.set(key, str(count['count']), ex=600)
            count = int(count['count'])
            lock.release()
        else:
            time.sleep(0.1)
            return count_all_posts(reload=reload)
    else:
        count = int(count)
    return count


def count_all_posts_for_query(q: str, reload=False):
    if q.strip() == '':
        return count_all_posts()
    redis = get_conn()
    key = 'global_post_count_for_query:' + q
    count = redis.get(key)
    if count is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if lock.acquire(blocking=False):
            cursor = get_cursor()
            query = "SET random_page_cost = 0.0001; SET LOCAL statement_timeout = 10000; "
            query += """
                SELECT COUNT(*)
                FROM (
                    SELECT * 
                    FROM posts 
                    WHERE 
                        content &@~ %s
                        AND ("user", service) NOT IN (SELECT id, service from dnp)
                    UNION
                    SELECT * 
                    FROM posts
                    WHERE
                        title &@~ %s
                        AND ("user", service) NOT IN (SELECT id, service from dnp)
                ) as UnionSearch;
            """
            cursor.execute(query, (q, q))
            count = cursor.fetchone()
            redis.set(key, str(count['count']), ex=600)
            count = int(count['count'])
            lock.release()
        else:
            time.sleep(0.1)
            return count_all_posts_for_query(q, reload=reload)
    else:
        count = int(count)
    return count


def get_all_posts(offset: int, limit=50, reload=False):
    redis = get_conn()
    key = 'all_posts:' + str(offset)
    all_posts = redis.get(key)
    if all_posts is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if lock.acquire(blocking=False):
            cursor = get_cursor()
            query = """
                SELECT *
                FROM posts
                WHERE ("user", service) NOT IN (SELECT id, service from dnp)
                ORDER BY added desc
                OFFSET %s
                LIMIT %s
            """
            cursor.execute(query, (offset, limit))
            all_posts = cursor.fetchall()
            redis.set(key, serialize_dict_list(all_posts), ex=600)
            lock.release()
        else:
            time.sleep(0.1)
            return get_all_posts(offset, reload=reload)
    else:
        all_posts = deserialize_dict_list(all_posts)
    return all_posts


def get_all_posts_for_query(q: str, offset: int, limit=50, reload=False):
    if q.strip() == '':
        return get_all_posts(0)
    redis = get_conn()
    key = 'all_posts_for_query:' + q + ':' + str(offset)
    results = redis.get(key)
    if results is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if lock.acquire(blocking=False):
            cursor = get_cursor()
            query = "SET random_page_cost = 0.0001; SET LOCAL statement_timeout = 10000; "
            query += """
                (
                    SELECT *
                    FROM posts
                    WHERE
                        content &@~ %s
                        AND ("user", service) NOT IN (SELECT id, service from dnp)
                ) UNION (
                    SELECT *
                    FROM posts
                    WHERE
                        title &@~ %s
                        AND ("user", service) NOT IN (SELECT id, service from dnp)
                ) ORDER BY added desc LIMIT %s OFFSET %s;
            """
            params = (q, q, limit, offset)

            cursor.execute(query, params)
            results = cursor.fetchall()
            redis.set(key, serialize_dict_list(results), ex=600)
            lock.release()
        else:
            time.sleep(0.1)
            return get_all_posts_for_query(q, offset, reload=reload)
    else:
        results = deserialize_dict_list(results)
    return results
