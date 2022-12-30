from src.utils.utils import limit_int, parse_int
from src.internals.types import PageProps
from src.lib.filehaus import (
    get_all_shares_count,
    get_files_for_share,
    get_shares,
    get_share
)

from flask import (
    Blueprint, make_response,
    render_template, request,
    redirect, url_for
)

filehaus = Blueprint('filehaus', __name__)


@filehaus.route('/share/<share_id>')
def get_share_page(share_id: str):
    base = request.args.to_dict()
    base.pop('o', None)

    props = dict(currentPage='shares')
    share = get_share(share_id)
    if share is None:
        response = redirect(url_for('filehaus.get_shares_page'))
        return response

    share_files = get_files_for_share(share['id'])

    response = make_response(render_template(
        'share.html',
        share_files=share_files,    
        share=share,
        props=props,
        base=base
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response


@filehaus.route('/shares')
def get_shares_page():
    base = request.args.to_dict()
    base.pop('o', None)

    offset = parse_int(request.args.get('o'), 0)  # noqa F811
    # query = request.args.get('q')
    limit = limit_int(int(request.args.get('limit') or 25), 50)

    shares = None
    total_count = None
    (shares, total_count) = get_share_page(offset, limit)

    props = dict(
        currentPage='shares',
        count=total_count,
        shares=shares,
        limit=limit
    )

    response = make_response(render_template(
        'shares.html',
        props=props,
        base=base,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response


def get_share_page(offset: int, limit: int):  # noqa F811
    posts = get_shares(offset, limit)
    total_count = get_all_shares_count()
    return (posts, total_count)
