from flask import Blueprint, request, make_response, render_template

from ..utils.utils import sort_dict_list_by, offset, take
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor
from ..internals.cache.redis import get_conn
from ..lib.artist import get_all_non_discord_artists

artists = Blueprint('artists', __name__)

@artists.route('/artists')
def get_artists():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    q = request.args.get('q')
    commit = request.args.get('commit')
    service = request.args.get('service')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order')
    offset = request.args.get('o')

    results = []
    count = 0
    if commit is not None:
        (results, props['count']) = get_search_results(q, service, sort_by, order, offset)

    response = make_response(render_template(
        'artists.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

def get_search_results(q, service, sort_by, order, o):
    artists = get_all_non_discord_artists()

    page = []
    matches = []
    if artists is not None:
        for artist in artists:
            try:
                artist['name'].index(q)
                matches.append(artist)
            except ValueError:
                continue

    if service:
        matches = filter(lambda artist: artist['service'] == service, matches)

    matches = sort_dict_list_by(matches, sort_by, order=='desc')
    
    if o is None:
        o = 0
    page = offset(matches, o)
    page = take(page, 25)

    return (page, len(matches))
