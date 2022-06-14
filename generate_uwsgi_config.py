import textwrap

from src.config import Configuration


def generate():
    opts = Configuration().webserver['uwsgi_options'].items()
    opts = '\n'.join(list(f'{k} = {v}' for k, v in opts))

    config_str = f'''
        [uwsgi]
        processes = { Configuration().webserver['workers'] }
        http = 0.0.0.0:{ Configuration().webserver['port'] }
        {'py-autoreload = 1' if Configuration().development_mode else ''}
        {opts}

        strict = true
        master = true
        vacuum = true
        single-interpreter = true
        die-on-term = true
        need-app = true
        lazy-apps = true
        enable-threads = true

        ; Worker recycling.
        max-requests = 0
        max-worker-lifetime = 3600
        reload-on-rss = 2048
        worker-reload-mercy = 60

        ; Harakiri (Longest amount of time an active worker can run without killing itself)
        harakiri = 60

        manage-script-name = true
        mount = /=server:app

        listen = 1000

        post-buffering = true
        buffer-size = 8192
    '''
    config_str = textwrap.dedent(config_str)
    config_str = config_str.strip()
    config_str += '\n'

    with open('uwsgi.ini', 'w') as f:
        f.write(config_str)


if __name__ == '__main__':
    generate()
