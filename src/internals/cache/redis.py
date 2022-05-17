import redis_lock
import dateutil
import datetime
import ujson
import copy
import rb

from flask import current_app
from os import getenv

from src.config import Configuration

cluster: rb.Cluster = None


class KemonoRouter(rb.BaseRouter):
    def get_host_for_key(self, key):
        top_level_prefix_of_key = key.split(':')[0]
        if (Configuration().redis['keyspaces'].get(top_level_prefix_of_key) is not None):
            return Configuration().redis['keyspaces'][top_level_prefix_of_key]
        else:
            raise rb.UnroutableCommand()


class KemonoRedisLock(redis_lock.Lock):
    ''' Reword to make the module compatible with Redis-Blaster. '''
    def release(self):
        if self._lock_renewal_thread is not None:
            self._stop_lock_renewer()
        # soft reimplementation of UNLOCK_SCRIPT in Python
        self._client.delete(self._signal)
        self._client.lpush(self._signal, 1)
        self._client.pexpire(self._signal, self._signal_expire)
        self._client.delete(self._name)

    def extend(self, expire=None):
        if expire:
            expire = int(expire)
            if expire < 0:
                raise ValueError("A negative expire is not acceptable.")
        elif self._expire is not None:
            expire = self._expire
        else:
            raise TypeError(
                "To extend a lock 'expire' must be provided as an "
                "argument to extend() method or at initialization time."
            )
        # soft reimplementation of EXTEND_SCRIPT in Python
        self._client.expire(self._name, expire)


def init():
    global cluster
    cluster = rb.Cluster(
        host_defaults=Configuration().redis['node_options'],
        hosts=dict((i, host) for i, host in enumerate(Configuration().redis['nodes'])),
        router_cls=KemonoRouter
    )
    return cluster


def get_conn():
    return cluster.get_routing_client()


def scan_keys(pattern):
    return cluster.get_local_client_for_key(pattern).scan_iter(match=pattern, count=5000)


def serialize_dict(data):
    to_serialize = {
        'dates': [],
        'data': {}
    }

    for key, value in data.items():
        if type(value) is datetime.datetime:
            to_serialize['dates'].append(key)
            to_serialize['data'][key] = value.isoformat()
        else:
            to_serialize['data'][key] = value

    return ujson.dumps(to_serialize)


def deserialize_dict(data):
    data = ujson.loads(data)
    to_return = {}
    for key, value in data['data'].items():
        if key in data['dates']:
            to_return[key] = dateutil.parser.parse(value)
        else:
            to_return[key] = value
    return to_return


def serialize_dict_list(data):
    data = copy.deepcopy(data)
    return ujson.dumps(list(map(lambda elem: serialize_dict(elem), data)))


def deserialize_dict_list(data):
    data = ujson.loads(data)
    to_return = list(map(lambda elem: deserialize_dict(elem), data))
    return to_return
