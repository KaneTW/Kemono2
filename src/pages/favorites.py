from flask import Blueprint, request, make_response, render_template, session, redirect, flash, url_for, current_app

from ..utils.utils import make_cache_key, get_value, restrict_value, sort_dict_list_by, take, offset
from ..lib.account import load_account
from ..lib.favorites import get_favorite_artists, get_favorite_posts, add_favorite_post, add_favorite_artist, remove_favorite_post, remove_favorite_artist
from ..lib.security import is_password_compromised
from ..internals.cache.flask_cache import cache

favorites = Blueprint('favorites', __name__)

@favorites.route('/favorites', methods=['GET'])
def list():
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))

    if account is not None:
        props = {}
        base = request.args.to_dict()
        base.pop('o', None)

        favorites = []
        fave_type = get_value(request.args, 'type', 'artist')
        if fave_type == 'post':
            favorites = get_favorite_posts(account['id'])
            sort_field = restrict_value(get_value(request.args, 'sort'), ['id', 'published'], 'id')
        else:
            favorites = get_favorite_artists(account['id'])
            sort_field = restrict_value(get_value(request.args, 'sort'), ['id', 'indexed'], 'id')

        offset = int(get_value(request.args, 'o', 0))
        sort_asc = True if get_value(request.args, 'order') == 'asc' else False
        results = sort_and_filter_favorites(favorites, offset, sort_field, sort_asc)

        props['fave_type'] = fave_type
        props['sort_field'] = sort_field
        props['sort_asc'] = sort_asc

        response = make_response(render_template(
            'favorites.html',
            props = props,
            base = base,
            source = 'account',
            results = results,
        ), 200)
        response.headers['Cache-Control'] = 's-maxage=60'
        return response
    else:
        props = {
            'currentPage': 'artists'
        }

        results = []
        if session.get('favorites'):
            for user in session['favorites']:
                service = user.split(':')[0]
                user_id = user.split(':')[1]

                cursor = get_cursor()

                if session.get('favorites_sort') == 'published' or not session or not session.get('favorites_sort'):
                    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s ORDER BY published desc LIMIT 1"
                elif session.get('favorites_sort') == 'added':
                    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s ORDER BY added desc LIMIT 1"
                params = (user_id, service)
                cursor.execute(query, params)
                latest_post = cursor.fetchone()

                cursor2 = get_cursor()
                query2 = "SELECT * FROM lookup WHERE id = %s AND service = %s"
                params2 = (user_id, service)
                cursor2.execute(query2, params2)
                results2 = cursor2.fetchone()

                if latest_post:
                    if latest_post.get('published') and (session.get('favorites_sort') == 'published' or not session or not session.get('favorites_sort')):
                        results.append({
                            "name": results2['name'] if results2 else "",
                            "service": service,
                            "user": user_id,
                            "delta_date": (latest_post['published'] - datetime.now()).total_seconds(),
                            "relative_date": relative_time(latest_post['published'])
                        })
                    elif session.get('favorites_sort') == 'added':
                        results.append({
                            "name": results2['name'] if results2 else "",
                            "service": service,
                            "user": user_id,
                            "delta_date": (latest_post['added'] - datetime.now()).total_seconds(),
                            "relative_date": relative_time(latest_post['added'])
                        })
                    else:
                        results.append({
                            "name": results2['name'] if results2 else "",
                            "service": service,
                            "user": user_id,
                            "delta_date": 99999999,
                            "error_msg": "Service unsupported."
                        })
                else:
                    results.append({
                        "name": results2['name'] if results2 else "",
                        "service": service,
                        "user": user_id,
                        "delta_date": 99999999,
                        "error_msg": "Never imported."
                    })
        
        props['phrase'] = "Last posted" if session.get('favorites_sort') == 'published' or not session.get('favorites_sort') else "Last imported"
        results.sort(key=delta_key, reverse=True)
        response = make_response(render_template(
            'favorites.html',
            props = props,
            source = 'session',
            results = results,
            session = session
        ), 200)
        response.headers['Cache-Control'] = 'no-store, max-age=0'
        return response

@favorites.route('/favorites/post/<service>/<artist_id>/<post_id>', methods=['POST'])
def post_favorite_post(service, artist_id, post_id):
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))
    add_favorite_post(account['id'], service, artist_id, post_id)
    return '', 200

@favorites.route('/favorites/artist/<service>/<artist_id>', methods=['POST'])
def post_favorite_artist(service, artist_id):
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))
    add_favorite_artist(account['id'], service, artist_id)
    return '', 200

@favorites.route('/favorites/post/<service>/<artist_id>/<post_id>', methods=['DELETE'])
def delete_favorite_post(service, artist_id, post_id):
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))
    remove_favorite_post(account['id'], service, artist_id, post_id)
    return '', 200

@favorites.route('/favorites/artist/<service>/<artist_id>', methods=['DELETE'])
def delete_favorite_artist(service, artist_id):
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))
    remove_favorite_artist(account['id'], service, artist_id)
    return '', 200

def sort_and_filter_favorites(favorites, o, field, asc):
    favorites = sort_dict_list_by(favorites, field, asc)
    return take(25, offset(o, favorites))
