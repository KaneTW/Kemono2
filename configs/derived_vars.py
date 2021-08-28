"""
Variables which are derivatives off environment variables go there.
"""

from .vars import flask_env

is_development = flask_env == 'development'
