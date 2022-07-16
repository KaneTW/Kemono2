import subprocess
import psycopg2
import sys
import os

import generate_tusker_config
import generate_uwsgi_config

from src.config import Configuration
from src.internals.database import database


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
        ''' Install client dependencies. '''
        if not os.path.isdir('./client/node_modules'):
            subprocess.run(
                ['npm', 'install'],
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

        try:
            if Configuration().automatic_migrations:
                ''' Run migrations. '''
                generate_tusker_config.run_migrations()

            ''' Initialize Pgroonga if needed. '''
            with database.pool.getconn() as conn:
                with conn.cursor() as db:
                    db.execute('CREATE EXTENSION IF NOT EXISTS pgroonga')
                    db.execute('CREATE INDEX IF NOT EXISTS pgroonga_posts_idx ON posts USING pgroonga (title, content)')
                    db.execute('CREATE INDEX IF NOT EXISTS pgroonga_comments_idx ON comments USING pgroonga (content)')
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
