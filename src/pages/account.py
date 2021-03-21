from flask import Blueprint, request, make_response, render_template, session, redirect, flash, url_for

from ..utils.utils import make_cache_key, get_value
from ..lib.account import get_login_info_for_username, load_account
from ..internals.cache.flask_cache import cache

import bcrypt

account = Blueprint('account', __name__)

@account.route('/login', methods=['GET'])
def get_login():
    account = load_account()
    if account is not None:
        return redirect(url_for('home.get_home'))

    response = make_response(render_template(
        'login.html',
        props = {}
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response
@account.route('/logout')
def logout():
    if 'account_id' in session:
        session.clear()
    return redirect(url_for('home.get_home'))

@account.route('/login', methods=['POST'])
def post_login():
    account = load_account()
    if account is not None:
        return redirect(url_for('home.get_home'))
    
    account = attempt_login(request.form)
    if account is None:
        flash('Username or password incorrect')
        return redirect(url_for('account.get_login'))

    session['account_id'] = account['id']
    return redirect(url_for('home.get_home'))

@account.route('/register')
def get_register():
    account = load_account()
    if account is not None:
        return redirect(url_for('home.get_home'))

    return make_response(render_template(
        'register.html',
        props = {}
    ), 200)

@account.route('/account')
def get_account():
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))

    return make_response(render_template(
        'account.html',
        props = {}
    ), 200)

def attempt_login(form):
    username = get_value(form, 'username')
    password = get_value(form, 'password')
    if username is None or password is None:
        return None

    account_info = get_login_info_for_username(username)
    if account_info is None:
        return None

    if bcrypt.checkpw(password, account_info['password_hash']):
        return load_account(account_info['id'])

    return None
