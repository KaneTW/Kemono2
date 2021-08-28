from flask import Blueprint, make_response, render_template

from ..lib.test_accounts import register_test_accounts, write_test_accounts_data

dev_only = Blueprint('dev-only', __name__)

@dev_only.route('/dev-only', methods=['GET'])
def main_page():
    props = {
        'currentPage': 'dev-only',
    }

    response = make_response(render_template(
        'dev_only/_index.html',
        props = props
    ), 200)
    return response

@dev_only.route('/dev-only', methods=['POST'])
def activate_dev_mode():
    accounts = register_test_accounts()
    print(f"Registered {len(accounts)} accounts.")
    is_saved = write_test_accounts_data(accounts)

    response = make_response(render_template(
        'success.html',
        props = {}
    ), 200)
    return response
    
