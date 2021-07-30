from typing import List
from ..internals.cache.redis import get_conn
from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..types.kemono import kemono_types
import ujson
import dateutil
import copy
import datetime

def get_unapproved_dms(import_id: str, reload: bool = False) -> List[kemono_types.DM]:
    redis = get_conn()
    key = 'unapproved_dms:' + import_id
    dms = redis.get(key)
    if dms is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM unapproved_dms WHERE import_id = %s'
        cursor.execute(query, (import_id,))
        dms = cursor.fetchall()
        redis.set(key, serialize_dms(dms), ex = 1)
    else:
        dms = deserialize_dms(dms)
    

    for i, dm in enumerate(dms):
        dms[i] = kemono_types.DM(
            id=dm["id"],
            user=dm["user"],
            service=dm["service"],
            content=dm["content"],
            added=dm["added"],
            published=dm["published"],
            embed=dm["embed"],
            file=dm["file"],
            import_id=dm["import_id"],
            contributor_id=dm["contributor_id"]
        )
    return dms

def get_artist_dms(service: str, artist_id: str, reload: bool = False):
    redis = get_conn()
    key = 'dms:' + service + ':' + str(artist_id)
    dms = redis.get(key)
    if dms is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM dms WHERE service = %s AND "user" = %s'
        cursor.execute(query, (service, artist_id))
        dms = cursor.fetchall()
        redis.set(key, serialize_dms(dms), ex = 600)
    else:
        dms = deserialize_dms(dms)
    return dms

def cleanup_unapproved_dms(import_id: str):
    cursor = get_cursor()
    query = 'DELETE FROM unapproved_dms WHERE import_id = %s'
    cursor.execute(query, (import_id,))

    return True

def approve_dm(import_id: str, dm_id: str):
    cursor = get_cursor()
    query = 'INSERT INTO dms (id, "user", service, content, embed, added, published, file) SELECT id, "user", service, content, embed, added, published, file FROM unapproved_dms WHERE import_id = %s AND id = %s; '
    query += 'DELETE FROM unapproved_dms WHERE import_id = %s AND id = %s;'
    cursor.execute(query, (import_id, dm_id, import_id, dm_id))

    return True

def serialize_dms(dms):
    dms = copy.deepcopy(dms)
    return ujson.dumps(list(map(lambda dm: prepare_dm_fields(dm), dms)))

def deserialize_dms(dms_str):
    dms = ujson.loads(dms_str)
    return list(map(lambda dm: rebuild_dm_fields(dm), dms))

def prepare_dm_fields(dm):
    dm['added'] = dm['added'].isoformat()
    dm['published'] = dm['published'].isoformat()
    return dm

def rebuild_dm_fields(dm):
    dm['added'] = dateutil.parser.parse(dm['added'])
    dm['published'] = dateutil.parser.parse(dm['published'])
    return dm
