from flask import Blueprint, request, make_response, render_template, session, redirect, flash, url_for, current_app

from ..utils.utils import make_cache_key, get_value, restrict_value, sort_dict_list_by
from ..lib.account import load_account, get_favorite_artists, get_favorite_posts
from ..lib.security import is_password_compromised
from ..internals.cache.flask_cache import cache

favorites = Blueprint('favorites', __name__)

@favorites.route('/favorites', methods=['GET'])
def list():
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))

    if account is not None:
        favorites = []
        fave_type = get_value(request.args, 'type')
        if fave_type == 'artist':
            favorites = get_favorite_artists(account['id'])
        else:
            favorites = get_favorite_posts(account['id'])

        sort_field = restrict_value(get_value(request.args, 'sort'), ['id', 'published'], 'id')
        sort_asc = True if get_value(request.args, 'dir') == '1' else False
        favorites = sort_favorites(favorites, fave_sort, sort_asc)

        response = make_response(render_template(
            'favorites.html',
            props = {},
            favorites = favorites,
            fave_type = fave_type
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
            results = results,
            session = session
        ), 200)
        response.headers['Cache-Control'] = 'no-store, max-age=0'
        return response

def sort_favorites(favorites, field, asc):
    return sort_dict_list_by(favorites, field, asc)
