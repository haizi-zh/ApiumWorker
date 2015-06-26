# coding=utf-8
import requests


__author__ = 'zephyre'


def get_etcd_host():
    import os

    val = os.getenv('ETCD_HOST')
    if val is None:
        print 'Cannot find environment variable ETCD_HOST, use "etcd" as default.'
        val = 'etcd'
    return val


def get_etcd_port():
    import os

    val = os.getenv('ETCD_PORT')
    if val is None:
        print 'Cannot find environment variable ETCD_PORT, use 2379 as default.'
        val = 2379
    else:
        val = int(val)
    return val


etcd_url = 'http://%s:%d' % (get_etcd_host(), get_etcd_port())


def get_service(service_name, alias):
    url = '%s/v2/keys/backends/%s' % (etcd_url, service_name)
    try:
        nodes = requests.get(url).json()['node']['nodes']
        values = nodes[0]['value'].split(':')
        host = values[0]
        port = int(values[1])
        return {alias: {'host': host, 'port': port}}
    except (KeyError, IndexError, ValueError):
        return None


_conf_map = {}


def build_conf(node, alias=None):
    current_key = alias or node['key'].split('/')[-1]
    if 'dir' in node and node['dir'] and 'nodes' in node and node['nodes']:
        m = {}
        for n in node['nodes']:
            m.update(build_conf(n))
        return {current_key: m}
    elif 'value' in node:
        return {current_key: node['value']}
    else:
        return None


def parse_cl_args():
    """
    解析命令行参数
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--module', '-m', nargs='*', choices=['sms'])
    parser.add_argument('--runlevel', choices=['production', 'dev', 'test'])
    extracted_args, left_over = parser.parse_known_args()

    args = sys.argv[:1]
    args.extend(left_over)

    return {'modules': extracted_args.module, 'runlevel': extracted_args.runlevel}, args


project_conf, cmd_args = parse_cl_args()


def get_config(service_names=None, conf_names=None, cache_key=None, force_refresh=False):
    if not force_refresh and cache_key and cache_key in _conf_map:
        return _conf_map[cache_key]

    def merge_dicts(*dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def build_tuple(val):
        """
        如果val形如(name, alias)，则返回(name, alias)
        如果val为一个字符串，比如service，则返回(service, service)
        其它情况：抛出ValueError
        """
        if isinstance(val, tuple) and len(val) == 2:
            return val
        elif isinstance(val, basestring):
            return val, val
        else:
            raise ValueError

    services = merge_dicts(*filter(lambda v: v, [get_service(*build_tuple(entry)) for entry in service_names]))

    conf_map = {}
    for entry in conf_names if conf_names is not None else []:
        name, alias = build_tuple(entry)
        url = '%s/v2/keys/project-conf/%s?recursive=true' % (etcd_url, name)
        data = requests.get(url).json()
        if 'node' not in data:
            continue
        else:
            conf_map.update(build_conf(data['node'], alias=alias))

    config = merge_dicts({'services': services}, conf_map, project_conf)

    if cache_key:
        _conf_map[cache_key] = config

    return config

