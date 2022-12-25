import sentry_sdk
import subprocess
import psycopg2
import logging
import sys
import os

import generate_tusker_config
import generate_uwsgi_config

from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from src.internals.database import database
from src.config import Configuration

if __name__ == '__main__':
    ''' Bugs to fix at a later time:                             '''
    '''     - Pages can get stuck with an older version of their '''
    '''       HTML, even after disabling anything and everything '''
    '''       related to cache. The only resolution as of now is '''
    '''       a restart of the entire webserver.                 '''

    environment_vars = {
        **os.environ.copy(),
        'FLASK_ENV': 'development' if Configuration().development_mode else 'production',
        'NODE_ENV': 'development' if Configuration().development_mode else 'production',
        'KEMONO_SITE': Configuration().webserver['site']
    }

    try:
        ''' Initialize Sentry. '''
        if Configuration().sentry_dsn:
            sentry_sdk.init(
                integrations=[FlaskIntegration(), RedisIntegration()],
                dsn=Configuration().sentry_dsn
            )

        ''' Install client dependencies. '''
        if not os.path.isdir('./client/node_modules'):
            subprocess.run(
                ['npm', 'ci', '--also=dev'],
                check=True,
                cwd='client',
                env=environment_vars
            )

        ''' Build or run client development server depending on config. '''
        if Configuration().development_mode:
            subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd='client',
                env=environment_vars
            )
        else:
            subprocess.run(
                ['npm', 'run', 'build'],
                check=True,
                cwd='client',
                env=environment_vars
            )

        database.init()
        try:
            if Configuration().automatic_migrations:
                ''' Run migrations. '''
                generate_tusker_config.run_migrations()

                ''' Initialize Pgroonga if needed. '''
                with database.pool.getconn() as conn:
                    with conn.cursor() as db:
                        db.execute('CREATE EXTENSION IF NOT EXISTS pgroonga')
                        db.execute('CREATE INDEX IF NOT EXISTS pgroonga_posts_idx ON posts USING pgroonga (title, content)')
                        db.execute('CREATE INDEX IF NOT EXISTS pgroonga_dms_idx ON dms USING pgroonga (content)')
                    conn.commit()
                    database.pool.putconn(conn)
        finally:
            ''' "Close" the database pool. '''
            database.close_pool()

        generate_uwsgi_config.generate()
        subprocess.run(['uwsgi', '--ini', './uwsgi.ini'], check=True, close_fds=True, env=environment_vars)
    except KeyboardInterrupt:
        sys.exit()
