from flask import Blueprint

from development.utils import static_page

design = Blueprint('design', __name__, url_prefix='/design')


@design.get('/')
def home_page():
    return static_page('development', 'development/design/home.html')


@design.get('/current')
def current_design():
    return static_page('development', 'development/design/current/home.html')


@design.get('/upcoming')
def upcoming_design():
    return static_page('development', 'development/design/upcoming/home.html')


@design.get('/wip')
def wip_design():
    return static_page('development', 'development/design/wip/home.html')
