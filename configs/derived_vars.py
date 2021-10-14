"""
Variables which are derivatives off environment variables go there.
"""

from .vars import flask_env, archiver_host, archiver_port

is_development = flask_env == 'development'
archiver_origin = f'http://{archiver_host}:{archiver_port}'
