import psycopg2
import textwrap
import os

from src.internals.database import database
from src.config import Configuration


def run_migration(migration) -> bool:
    database.init()
    with open(os.path.join('migrations', migration)) as f:
        for query in f.read().split(';'):
            query = query.strip()
            if query and not query.startswith('--') and not query.startswith('#'):
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
                    database.pool.putconn(conn)

    return True


def generate():
    config_str = f'''
        [schema]
        filename = "schema.sql"

        [migrations]
        directory = "migrations"

        [database]
        host = "{Configuration().database['host']}"
        port = {Configuration().database['port']}
        user = "{Configuration().database['user']}"
        password = "{Configuration().database['password']}"
        dbname = "{Configuration().database['database']}"

        [migra]
        safe = false
        privileges = false
    '''
    config_str = textwrap.dedent(config_str)
    config_str = config_str.strip()
    config_str += '\n'

    with open('tusker.toml', 'w') as f:
        f.write(config_str)


def run_migrations():
    generate()
    for migration in os.listdir('migrations'):
        run_migration(migration)


if __name__ == '__main__':
    generate()
