from flask import Blueprint, request, make_response, render_template

Home = Blueprint('Home', __name__)

@Home.route('/')
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
