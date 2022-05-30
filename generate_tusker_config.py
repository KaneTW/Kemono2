import textwrap

from src.config import Configuration


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


if __name__ == '__main__':
    generate()
