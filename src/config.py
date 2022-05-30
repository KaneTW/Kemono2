import multiprocessing
import getpass
import random
import string
import json
import os


class Configuration:
    def __init__(self):
        config_file = os.environ.get('KEMONO_CONFIG') or 'config.json'
        config_location = os.path.join('./', config_file)
        config = {}

        if os.path.exists(config_location):
            with open(config_location) as f:
                config = json.loads(f.read())

        self.site = config.get('site', 'http://localhost:6942')
        self.development_mode = config.get('development_mode', True)
        self.automatic_migrations = config.get('automatic_migrations', True)

        ''' Configuration for the frontend server. '''
        self.webserver = config.get('webserver', {})
        # Secret key used to encrypt sessions.
        self.webserver['secret'] = self.webserver.get('secret', ''.join(random.choice(string.ascii_letters) for _ in range(32)))
        # How many workers and threads should run at once?
        self.webserver['workers'] = self.webserver.get('workers', multiprocessing.cpu_count())
        self.webserver['threads'] = self.webserver.get('threads', 2)
        # If you've dealt with how the trust of forwarding IPs works upstream, flip this off.
        self.webserver['ip_security'] = self.webserver.get('ip_security', True)
        # Set additional Gunicorn options if you want. Overrides any of the other options.
        self.webserver['gunicorn_options'] = self.webserver.get('gunicorn_options', {
            # Default here will kill workers after a certain amount of requests.
            # "Jitter" helps with timing, so your site doesn't down itself during a purge.
            # Recommended if you are running in production; keeps memory clean.
            'max-requests': 1000,
            'max-requests-jitter': 10
        })
        # The port the site will be served on.
        self.webserver['port'] = self.webserver.get('port', 6942)
        # The location of the resources that will be served.
        self.webserver['static_folder'] = self.webserver.get(
            'static_folder',
            'client/dev/static' if self.development_mode else 'dist/static'
        )
        self.webserver['template_folder'] = self.webserver.get(
            'template_folder',
            'client/dev/pages' if self.development_mode else 'dist/pages'
        )

        self.database = config.get('database', {})
        self.database['host'] = self.database.get('host', '127.0.0.1')
        self.database['port'] = self.database.get('port', 5432)
        self.database['password'] = self.database.get('password', '')
        self.database['database'] = self.database.get('database', 'postgres')
        try:
            self.database['user'] = self.database.get('user', getpass.getuser())
        except:
            self.database['user'] = self.database.get('user', 'shinonome')

        self.redis = config.get('redis', {})
        self.redis['node_options'] = self.redis.get('defaults', {
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0
        })
        self.redis['nodes'] = self.redis.get('nodes', [{"db": 0}])
        self.redis['keyspaces'] = self.redis.get('keyspaces', {
            "account": 0,
            "saved_key_import_ids": 0,
            "saved_keys": 0,
            "top_artists": 0,
            "artists_faved": 0,
            "artists_faved_count": 0,
            "top_artists_recently": 0,
            "artists_recently_faved_count": 0,
            "random_artist_keys": 0,
            "non_discord_artist_keys": 0,
            "non_discord_artists": 0,
            "artists_by_service": 0,
            "artist": 0,
            "artist_post_count": 0,
            "artist_last_updated": 0,
            "artists_by_update_time": 0,
            "unapproved_dms": 0,
            "dms": 0,
            "all_dms": 0,
            "all_dms_count": 0,
            "all_dms_by_query": 0,
            "all_dms_by_query_count": 0,
            "dms_count": 0,
            "favorite_artists": 0,
            "favorite_posts": 0,
            "artist_favorited": 0,
            "post_favorited": 0,
            "posts_by_favorited_artists": 0,
            "notifications_for_account": 0,
            "random_post_keys": 0,
            "all_post_keys": 0,
            "post": 0,
            "comments": 0,
            "posts_by_artist": 0,
            "artist_posts_offset": 0,
            "is_post_flagged": 0,
            "next_post": 0,
            "previous_post": 0,
            "importer_logs": 0,
            "ratelimit": 0,
            "all_posts": 0,
            "all_posts_for_query": 0,
            "global_post_count": 0,
            "global_post_count_for_query": 0,
            "lock": 0,
            "lock-signal": 0,
            "imports": 0,
            "running_imports": 0
        })
