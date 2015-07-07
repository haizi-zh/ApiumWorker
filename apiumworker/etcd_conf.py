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
    """
    获得服务的入口信息（host:port）

    所谓服务，是指etcd的服务发现部分的数据，比如：http://etcd:2379/v2/keys/backends/mongo?recursive=true
    上面一条数据中，记录了一组MongoDB服务器的入口地址。之所以是一组而不是一个，是为了高可用扩展的需求。

    上述服务的service_name为mongo。默认情况下，如果将该服务读入系统配置，其配置名就是services.mongo。
    在这里，我们可以对其取一个别名，比如mongodb-alias，那么该服务在系统配置中的键就是services.mongodb-alias

    :param service_name: 服务名称
    :param alias: 服务别名
    :return:
    """
    url = '%s/v2/keys/backends/%s' % (etcd_url, service_name)

    def get_service_entry(entry):
        """
        获得单一服务器地址

        比如，entry数据为：
        {"key":"/backends/mongo/ec6f787e91762f28741d01d6e0e7841c395f5f3ddcfa07db1c873e3a7ad6e6b3",
        "value":"192.168.100.2:31001","expiration":"2015-07-07T01:46:31.757230168Z","ttl":18,
        "modifiedIndex":5703768,"createdIndex":5703768}

        则返回一个tuple：("ec6f787e91762f28741d01d6e0e7841c395f5f3ddcfa07db1c873e3a7ad6e6b3", {"host": "192.168.100.2", "port": 31001})
        这在复制集的情况下很有用
        """
        key = entry['key'].split('/')[-1]
        value = entry['value'].split(':')
        host = value[0]
        port = int(value[1])

        return key, {'host': host, 'port': port}

    try:
        nodes = requests.get(url).json()['node']['nodes']
        return {alias: dict(map(get_service_entry, nodes))}
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
    parser.add_argument('--module', '-m', nargs='*', choices=['sms', 'contact'])
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

