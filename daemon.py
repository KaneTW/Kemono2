import subprocess
import gunicorn
import sys
import os

from src.config import Configuration

if __name__ == '__main__':
    ''' Bugs to fix at a later time:                             '''
    '''     - Pages can get stuck with an older version of their '''
    '''       HTML, even after disabling anything and everything '''
    '''       related to cache. The only resolution as of now is '''
    '''       a restart of the entire webserver.                 '''

    try:
        if not os.path.isdir('./client/node_modules'):
            subprocess.run(
                ['npm', 'install'],
                check=True,
                cwd='client'
            )

        if Configuration().development_mode:
            subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd='client'
            )
        else:
            subprocess.run(
                ['npm', 'run', 'build'],
                check=True,
                cwd='client'
            )

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
        ''', shell=True, check=True)
    except KeyboardInterrupt:
        sys.exit()
