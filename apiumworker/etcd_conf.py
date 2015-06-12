import os

import requests


__author__ = 'zephyre'

etcd_host = os.getenv('ETCD_HOST', 'etcd')
etcd_port = int(os.getenv('ETCD_PORT', 2379))
etcd_url = 'http://%s:%d' % (etcd_host, etcd_port)


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def get_service(service_name):
    url = '%s/v2/keys/backends/%s' % (etcd_url, service_name)
    try:
        nodes = requests.get(url).json()['node']['nodes']
        values = nodes[0]['value'].split(':')
        host = values[0]
        port = int(values[1])
        return {service_name: {'host': host, 'port': port}}
    except (KeyError, IndexError, ValueError):
        return None


def build_conf(node):
    current_key = node['key'].split('/')[-1]
    if 'dir' in node and node['dir'] and 'nodes' in node and node['nodes']:
        m = {}
        for n in node['nodes']:
            m.update(build_conf(n))
        return {current_key: m}
    elif 'value' in node:
        return {current_key: node['value']}
    else:
        return None


def get_config(service_names=None, conf_names=None):
    import requests

    services = merge_dicts(*filter(lambda v: v, [get_service(s) for s in service_names]))

    conf_map = {}
    for name in conf_names if conf_names is not None else []:
        url = '%s/v2/keys/project-conf/%s?recursive=true' % (etcd_url, name)
        data = requests.get(url).json()
        if 'node' not in data:
            continue
        else:
            conf_map.update(build_conf(data['node']))

    return {'services': services, 'conf': conf_map}

