from flask import session

from ..internals.database.database import get_cursor

import ujson
import copy

account_create_lock = Lock()

def load_account(account_id = None, reload = False):
    if account_id is None and 'account_id' in session:
        print("in session: " + session['account_id'])
        return load_account(session['account_id'], reload)
    elif account_id is None and 'account_id' not in session:
        return None

    key = 'account:' + account_id
    account = redis.get(key)
    if account is None or reload:
        cursor = get_cursor()
        query = 'select id, username, created_at from account where id = %s'
        cursor.execute(query, (account_id,))
        account = cursor.fetchone()
        redis.set(key, serialize_account(account))
    else:
        account = deserialize_account(account)

    return account

def get_favorite_artists(account_id = None, reload = False):
    key = 'favorite_artists:' + account_id
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = 'select post_id from account_artist_favorite where account_id = %s order by id desc'
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_favorites(favorites))
    else:
        favorites = deserialize_favorites(favorites)

    return favorites

def get_favorite_posts(account_id = None, reload = False):
    key = 'favorite_posts:' + account_id
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = 'select post_id from account_post_favorite where account_id = %s order by id desc'
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_favorites(favorites))
    else:
        favorites = serialize_favorites(favorites)

    return favorites

def get_login_info_for_username(username):
    cursor = get_cursor()
    query = 'select id, password_hash from account where username = %s'
    cursor.execute(query, (username,))
    return cursor.fetchone()

def is_logged_in():
    if 'account_id' in session:
        return True
    return False

def is_username_taken(username):
    cursor = get_cursor()
    query = 'select id from account where username = %s'
    cursor.execute(query, (username,))
    return cursor.fetchone() is not None

def create_account(username, password, favorites):
    account_id = None
    account_create_lock.acquire()
    try:
        if is_username_taken(username):
            return False

        cursor = get_cursor()
        query = "insert into account (username, password_hash) values (%s, %s) returning id"
        cursor.execute(query, (username, password_hash,))
        account_id = cursor.fetchone()[0]
    finally:
        account_create_lock.release()

    favorites = get_value(session, 'favorites')
    if favorites is not None:
        for user in favorites:
            service = user.split(':')[0]
            user_id = user.split(':')[1]
            add_favorite_artist(account_id, service, user_id)

def add_favorite_artist(account_id, service, user_id):
    cursor = get_cursor()
    query = 'insert into account_artist_favorite (account_id, service, artist_id) values (%s, %s, %s)'
    cursor.execute(query, (account_id, service, artist_id,))
    get_favorites(account_id, True)

def serialize_favorites(favorites):
    return ujson.dumps(favorites)

def deserialize_favorites(favorites):
    return ujson.loads(favorites)

def serialize_account(account):
    account = copy.deepcopy(account)
    return ujson.dumps(prepare_account_fields(account))

def deserialize_account(account):
    account = ujson.loads(account)
    return rebuild_account_fields(account)

def prepare_account_fields(account):
    account['created_at'] = account['created_at'].isoformat()
    return account

def rebuild_account_fields(account):
    account['created_at'] = dateutil.parser.parse(account['indexed'])
    return created_at
