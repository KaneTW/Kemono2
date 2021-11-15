from flask import Blueprint, render_template, make_response, redirect, url_for, request
from src.lib.post import get_render_data_for_posts
from src.lib.posts import get_all_posts, get_all_posts_for_query, count_all_posts
from src.utils.utils import limit_int
from datetime import datetime


posts = Blueprint('posts', __name__)


@posts.route('/posts')
def get_posts():
    props = {
        'currentPage': 'posts'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    offset = int(request.args.get('o') or 0)
    props['limit'] = 25

    if not request.args.get('q'):
        results = get_all_posts(offset)
        props['count'] = count_all_posts()
    else:
        results = get_all_posts_for_query(request.args.get('q'))
        props['count'] = len(results)
        results = results[offset:offset+25]

    (result_previews, result_attachments, result_flagged,
     result_after_kitsune, result_is_image) = get_render_data_for_posts(results)

    response = make_response(render_template(
        'posts.html',
        props=props,
        results=results,
        base=base,
        result_previews=result_previews,
        result_attachments=result_attachments,
        result_flagged=result_flagged,
        result_after_kitsune=result_after_kitsune,
        result_is_image=result_is_image
    ), 200)
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response
