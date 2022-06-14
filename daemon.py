import generate_tusker_config
import subprocess
import gunicorn
import psycopg2
import sys
import os

from src.config import Configuration
from src.internals.database import database


def run_migration(migration) -> bool:
    with open(os.path.join('migrations', migration)) as f:
        for query in f.read().split(';'):
            query = query.strip()
            if query:
                with database.pool.getconn() as conn:
                    with conn.cursor() as db:
                        try:
                            db.execute(query)
                        except psycopg2.Error as e:
                            # https://www.postgresql.org/docs/current/errcodes-appendix.html
                            if str(e.pgcode) in ['42P07', '42710', '55000']:
                                ''' Ignore errors about tables or constraints already existing. '''
                                continue
                            raise
                    conn.commit()
    return True


if __name__ == '__main__':
    ''' Bugs to fix at a later time:                             '''
    '''     - Pages can get stuck with an older version of their '''
    '''       HTML, even after disabling anything and everything '''
    '''       related to cache. The only resolution as of now is '''
    '''       a restart of the entire webserver.                 '''

    environment_vars = {
        'FLASK_ENV': 'development' if Configuration().development_mode else 'production',
        'NODE_ENV': 'development' if Configuration().development_mode else 'production',
        'KEMONO_SITE': Configuration().webserver['site']
    }

    try:
        if not os.path.isdir('./client/node_modules'):
            subprocess.run(
                ['npm', 'install'],
                check=True,
                cwd='client',
                env=environment_vars
            )

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

        if Configuration().automatic_migrations:
            ''' Generate Tusker config... '''
            generate_tusker_config.generate()

            ''' ...and run migrations. '''
            database.init()
            for migration in os.listdir('migrations'):
                run_migration(migration)

        opts = Configuration().webserver['gunicorn_options'].items()
        opts = ' '.join(list(f'--{k} {v}' for k, v in opts))
        if not Configuration().webserver['ip_security']:
            opts += ' --forwarded_allow_ips=*'
            opts += ' --proxy_allow_ips=*'
        subprocess.run(f'''
            gunicorn \\
                { '--reload' if Configuration().development_mode else '' } \\
                --workers { Configuration().webserver['workers'] } \\
                --threads { Configuration().webserver['threads'] } \\
                {opts} \\
                -b 0.0.0.0:{ Configuration().webserver['port'] } \\
            server:app
        ''', shell=True, check=True, close_fds=True, env=environment_vars)
    except KeyboardInterrupt:
        sys.exit()
