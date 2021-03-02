from flask import Blueprint, request, make_response, render_template

from .internals.utils.utils import make_cache_key
from .internals.utils.flask_cache import cache

Home = Blueprint('Home', __name__)

@Home.route('/')
@cache.cached(key_prefix=make_cache_key)
def home():
    props = {}
    base = request.args.to_dict()
    base.pop('o', None)
    response = make_response(render_template(
        'home.html',
        props = props,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response
