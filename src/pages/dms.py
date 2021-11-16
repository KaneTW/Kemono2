from flask import Blueprint, request, make_response, render_template

from ..utils.utils import sort_dict_list_by, offset, take, limit_int, parse_int
from ..lib.dms import get_all_dms, get_all_dms_by_query, get_all_dms_count, get_all_dms_by_query_count
from ..lib.artist import get_artist
dms = Blueprint('dms', __name__)

@dms.route('/dms')
def get_dms():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)
    
    offset = parse_int(request.args.get('o'), 0)
    query = request.args.get('q')
    limit = limit_int(int(request.args.get('limit') or 25), 50)
    
    if query is None:
        (dms, total_count) = get_dm_page(offset, limit)
    else:
        (dms, total_count) = do_dm_search(query, offset, limit)

    artists = list(get_artist(dm.service, dm.user) for dm in dms)

    props['count'] = total_count
    props['limit'] = limit

    response = make_response(render_template(
        'all_dms.html',
        props = props,
        base = base,
        dms = dms,
        artists = artists
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

def get_dm_page(offset, limit):
    posts = get_all_dms(offset, limit)
    total_count = get_all_dms_count()
    return (posts, total_count)

def do_dm_search(q, offset, limit):
    posts = get_all_dms_by_query(q, offset, limit)
    total_count = get_all_dms_by_query_count(q)
    return (posts, total_count)