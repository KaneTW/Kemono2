from flask import session

from ..internals.database.database import get_cursor

import ujson
import copy

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

def get_favorites(account_id = None, reload = False):
    key = 'favorites:' + account_id
    favorites = redis.get(key)
    if favorites is None or reload:
        cursor = get_cursor()
        query = 'select post_id from account_favorite where account_id = %s order by id desc'
        cursor.execute(query, (account_id,))
        favorites = cursor.fetchall()
        redis.set(key, serialize_favorites(favorites))
    else:
        favorites = deserialize_account(favorites)

def get_login_info_for_username(username):
    cursor = get_cursor()
    query = 'select id, password_hash from account where username = %s'
    cursor.execute(query, (username,))
    return cursor.fetchone()

def is_logged_in():
    if 'account_id' in session:
        return True
    return False

def serialize_favorites(favorites):
    return ujson.dumps(favorites)

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
