import functools
import dill
import time

from .redis import get_conn, KemonoRedisLock
from contextlib import nullcontext


def cache(prefix, ttl=3600, lock=True):
    def cache_decorator(func):
        @functools.wraps(func)
        def cache_wrapper(*args, **kwargs):
            reload = kwargs.pop('reload', False)
            redis = get_conn()
            key = prefix
            if len(args):
                key_args = ':'.join(str(arg) for arg in args)
                key += f':{key_args}'
            if len(kwargs):
                key_kwargs = ':'.join(str(kwarg) for kwarg in kwargs)
                key += f':{key_kwargs}'
            result = redis.get(key)
            if result is None or reload:
                rlock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)
                if lock and not rlock.acquire(blocking=False):
                    time.sleep(0.1)
                    return cache_wrapper(*args, **kwargs)
                result = func(*args, **kwargs)
                redis.set(key, dill.dumps(result), ex=ttl)
                if lock:
                    rlock.release()
            else:
                result = dill.loads(result)
            return result
        return cache_wrapper
    return cache_decorator
