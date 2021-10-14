import requests
from flask import Blueprint, make_response, render_template, g, redirect, url_for, current_app

from configs.derived_vars import archiver_origin
from src.dev_only.lib.test_accounts import register_test_accounts, write_test_accounts_data

from src.types.account import Account
from src.types.props import SuccessProps

dev_only = Blueprint('dev-only', __name__)

@dev_only.before_request
def check_creds():
    if not g.get('account'):
        return redirect(url_for('account.get_login'))

@dev_only.get('/dev-only')
def main_page():
    props = {
        'currentPage': 'dev-only',
    }

    response = make_response(render_template(
        'dev_only/_index.html',
        props = props
    ), 200)
    return response

@dev_only.post('/dev-only')
def activate_dev_mode():
    accounts = register_test_accounts()
    print(f"Registered {len(accounts)} accounts.")
    is_saved = write_test_accounts_data(accounts)

    props = SuccessProps(currentPage= 'dev-only', redirect= 'dev-only')

    response = make_response(render_template(
        'success.html',
        props = props
    ), 200)
    return response

@dev_only.post('/dev-only/service-keys')
def generate_service_keys():
    account: Account = g.account
    try:
        request = requests.post(
            url= f"{archiver_origin}/development/service-keys",
            data= dict(
                account_id = str(account.id)
            )
        )
        request.raise_for_status()
        props = SuccessProps(currentPage= 'dev-only', redirect= '/dev-only')

        response = make_response(render_template(
            'success.html',
            props = props
        ), 200)
        return response

    except Exception as e:
        current_app.logger.exception('Error connecting to archver')
        return f'Error while connecting to archiver. Is it running?', 500
