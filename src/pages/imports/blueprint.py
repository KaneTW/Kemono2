import json
from src.internals.cache.redis import (
    deserialize_dict,
    serialize_dict,
    scan_keys,
    get_conn,
)
from src.lib.imports import validate_import_key
from src.utils.utils import get_import_id

from flask import (
    Blueprint,
    current_app,
    g,
    make_response,
    render_template,
    request,
    session
)
from src.lib.dms import approve_dm, cleanup_unapproved_dms, get_unapproved_dms
from src.types.kemono import Unapproved_DM
from src.types.props import SuccessProps
from .types import DMPageProps, StatusPageProps, ImportProps

importer_page = Blueprint('importer_page', __name__)


@importer_page.get('/importer')
def importer():
    props = ImportProps()

    response = make_response(render_template(
        'importer_list.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response


@importer_page.get('/importer/tutorial')
def importer_tutorial():
    props = ImportProps()

    response = make_response(render_template(
        'importer_tutorial.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response


@importer_page.get('/importer/ok')
def importer_ok():
    props = ImportProps()

    response = make_response(render_template(
        'importer_ok.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response


@importer_page.get('/importer/status/<import_id>')
def importer_status(import_id):
    is_dms = bool(request.args.get('dms'))

    props = StatusPageProps(
        import_id=import_id,
        is_dms=is_dms
    )
    response = make_response(render_template(
        'importer_status.html',
        props=props
    ), 200)

    response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
    return response


@importer_page.get('/importer/dms/<import_id>')
def importer_dms(import_id: str):
    account_id: str = session.get('account_id')
    dms = get_unapproved_dms(import_id, account_id) if account_id else []

    props = DMPageProps(
        import_id=import_id,
        account_id=account_id,
        dms=dms
    )

    response = make_response(render_template(
        'importer/dms.html',
        props=props,
    ), 200)

    response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
    return response


@importer_page.post('/importer/dms/<import_id>')
def approve_importer_dms(import_id):
    props = SuccessProps(
        currentPage="import",
        redirect=f'/importer/status/{import_id}'
    )
    SuccessProps
    approved_ids = request.form.getlist('approved_ids')
    for dm_id in approved_ids:
        approve_dm(import_id, dm_id)
    cleanup_unapproved_dms(import_id)

    response = make_response(render_template(
        'success.html',
        props=props
    ), 200)

    response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
    return response


@importer_page.route('/api/logs/<import_id>')
def get_importer_logs(import_id: str):
    redis = get_conn()
    key = f'importer_logs:{import_id}'
    llen = redis.llen(key)
    messages = []
    if llen > 0:
        messages = redis.lrange(key, 0, llen)
        redis.expire(key, 60 * 60 * 48)

    return json.dumps(list(map(lambda msg: msg.decode('utf-8'), messages))), 200


# API
# TODO: move into separate blueprint
@importer_page.post('/api/import')
def importer_submit():
    if not session.get('account_id') and request.form.get("save_dms"):
        return 'You must be logged in to import direct messages.', 401

    if not request.form.get("session_key"):
        return "Session key missing.", 401

    key = request.form.get("session_key").strip()
    result = validate_import_key(key, request.form.get("service"))

    if not result.is_valid:
        return ("\n".join(result.errors), 422)

    formatted_key = result.modified_result if result.modified_result else key

    try:
        redis = get_conn()

        for _import in scan_keys('imports:*'):
            _import = _import.decode('utf8')
            existing_import = redis.get(_import)
            existing_import_data = json.loads(existing_import)
            if existing_import_data['key'] == formatted_key:
                props = SuccessProps(
                    message='This key is already being used for an import. Redirecting to logs...',
                    currentPage='import',
                    redirect=f"/importer/status/{_import.split(':')[1]}{ '?dms=1' if request.form.get('save_dms') else '' }"
                )

                return make_response(render_template(
                    'success.html',
                    props=props
                ), 200)

        import_id = get_import_id(formatted_key)
        data = dict(
            key=formatted_key,
            service=request.form.get("service"),
            channel_ids=request.form.get("channel_ids"),
            auto_import=request.form.get("auto_import"),
            save_session_key=request.form.get("save_session_key"),
            save_dms=request.form.get("save_dms"),
            contributor_id=session.get("account_id"),
            priority=1
        )
        redis.set(f'imports:{import_id}', json.dumps(data))

        props = SuccessProps(
            currentPage='import',
            redirect=f'/importer/status/{import_id}{"?dms=1" if request.form.get("save_dms") else "" }'
        )

        return make_response(render_template(
            'success.html',
            props=props
        ), 200)
    except Exception:
        current_app.logger.exception('Error connecting to archiver')
        return 'Error while pushing import request. Is Redis running?', 500
