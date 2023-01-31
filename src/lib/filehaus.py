from ..internals.cache.redis import get_conn, KemonoRedisLock
from ..internals.database.database import get_cursor

import json
import time
import dill


def get_share(share_id: int, reload=False):
    redis = get_conn()
    key = 'share:' + str(share_id)
    share = redis.get(key)
    if share is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if not lock.acquire(blocking=False):
            time.sleep(0.1)
            return get_share(share_id, reload=reload)

        cursor = get_cursor()
        query = """
            SELECT *
            FROM shares
            WHERE id = %(id)s
        """
        cursor.execute(query, dict(id=share_id))
        share = cursor.fetchone()
        redis.set(key, dill.dumps(share), ex=600)
    else:
        share = dill.loads(share)

    return share


def get_shares(offset: int, limit=50, reload=False):
    redis = get_conn()
    key = 'all_shares:' + str(offset) + ':'
    shares = redis.get(key)
    if shares is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if not lock.acquire(blocking=False):
            time.sleep(0.1)
            return get_shares(offset, limit=limit, reload=reload)

        cursor = get_cursor()
        query = """
            SELECT *
            FROM shares
            OFFSET %(offset)s
            LIMIT %(limit)s
        """
        cursor.execute(query, {
            'offset': offset,
            'limit': limit
        })
        shares = cursor.fetchall()
        redis.set(key, dill.dumps(shares), ex=600)
    else:
        shares = dill.loads(shares)

    return shares


def get_all_shares_count(reload: bool = False) -> int:
    redis = get_conn()
    key = 'all_shares_count'
    count = redis.get(key)

    if count and not reload:
        return int(count)

    lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return get_all_shares_count(reload=reload)

    cursor = get_cursor()
    query = """
        SELECT COUNT(*)
        FROM shares
    """
    cursor.execute(query)
    count = int(cursor.fetchone()['count'])
    redis.set(key, str(count), ex=600)
    lock.release()

    return count


def get_artist_shares(artist_id, service, sort='id', reload=False):
    redis = get_conn()
    key = 'artist_shares:' + service + ':' + str(artist_id)
    shares = redis.get(key)
    if shares is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if not lock.acquire(blocking=False):
            time.sleep(0.1)
            return get_artist_shares(artist_id, service, sort, reload)

        cursor = get_cursor()
        query = """
            SELECT *
            FROM shares
            WHERE id IN (
                SELECT share_id
                FROM lookup_share_relationships
                WHERE
                    user_id = %(artist_id)s
                    AND service = %(service)s
            );
        """
        cursor.execute(query, dict(
            artist_id=artist_id,
            service=service
        ))
        shares = cursor.fetchall()
        redis.set(key, dill.dumps(shares), ex=600)
    else:
        shares = dill.loads(shares)

    return shares


def get_files_for_share(share_id: int, reload=False):
    redis = get_conn()
    key = 'share_files:' + str(share_id)
    files = redis.get(key)
    if files is None or reload:
        lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
        if not lock.acquire(blocking=False):
            time.sleep(0.1)
            return get_files_for_share(share_id, reload=reload)

        cursor = get_cursor()
        query = """
            SELECT *
            FROM file_share_relationships fsr
            LEFT JOIN files f
            ON fsr.file_id = f.id
            WHERE share_id = %(share_id)s;
        """
        cursor.execute(query, {'share_id': share_id})
        files = cursor.fetchall()
        redis.set(key, dill.dumps(files), ex=600)
    else:
        files = dill.loads(files)

    return files
