from flask import Blueprint, request, make_response, render_template, abort

from src.lib.account import load_account

from .types import mod_props

moderator = Blueprint('mod', __name__)

@moderator.before_request
def check_credentials():
    account = load_account()
    if (not account or account['role'] != 'moderator'):
        return abort(404)

@moderator.get('/moderator')
def get_dashboard():
    props = mod_props.Dashboard()

    response = make_response(render_template(
        'account/moderator/dashboard.html',
        props = props,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response
    

# @moderator.route("/mod/tasks/files")
# def get_files():
#     files = []
#     props = mod_props.Files(
#         files= files
#     )
#     response = make_response(render_template(
#         'moderator_files.html',
#         props = props,
#     ), 200)
#     response.headers['Cache-Control'] = 's-maxage=60'
#     return response
