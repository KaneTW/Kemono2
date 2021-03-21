from flask import Blueprint, request, make_response, render_template, session, redirect, flash, url_for

from ..utils.utils import make_cache_key, get_value
from ..lib.account import get_login_info_for_username, load_account, is_username_taken, attempt_login, create_account
from ..lib.security import is_password_compromised
from ..internals.cache.flask_cache import cache

import bcrypt
from threading import Lock

account = Blueprint('account', __name__)

@account.route('/account/login', methods=['GET'])
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

@account.route('/account/login', methods=['POST'])
def post_login():
    account = load_account()
    if account is not None:
        return redirect(url_for('home.get_home'))
    
    username = get_value(request.form, 'username')
    password = get_value(request.form, 'password')
    account = attempt_login(username, password)
    if account is None:
        flash('Username or password incorrect')
        return redirect(url_for('account.get_login'))

    session['account_id'] = account['id']
    return redirect(url_for('home.get_home'))

@account.route('/account/logout')
def logout():
    if 'account_id' in session:
        session.clear()
    return redirect(url_for('home.get_home'))

@account.route('/account/register', methods=['GET'])
def get_register():
    account = load_account()
    if account is not None:
        return redirect(url_for('home.get_home'))

    return make_response(render_template(
        'register.html',
        props = {}
    ), 200)

@account.route('/account/register', methods=['POST'])
def post_register():
    username = get_value(request.form, 'username')
    password = get_value(request.form, 'password')
    confirm_password = get_value(request.form, 'confirm_password')

    errors = False
    if password != confirm_password:
        flash('Passwords do not match')
        errors = True

    if is_username_taken(username):
        flash('Username already taken')
        errors = True

    if is_password_compromised(password):
        flash('We\'ve detected that password was compromised in a data breach on another site. Please choose a different password.')
        errors = True

    if not errors:
        success = create_account(username, password)
        if not success:
            flash('Username already taken')
            errors = True

    if not errors:
        account = attempt_login(username, password)
        if account is None:
            current.app.logger.warning("Error logging into account immediately after creation")
        flash('Account created successfully')
        return redirect(url_for('artists.list'))

    return redirect(url_for('account.get_register'))

@account.route('/account')
def get_account():
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))

    return make_response(render_template(
        'account.html',
        props = {}
    ), 200)
