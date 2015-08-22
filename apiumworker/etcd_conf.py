# coding=utf-8
import requests
from requests.exceptions import RequestException


__author__ = 'zephyre'


# 缓存的配置信息
cached_conf_map = {}


def get_etcd_endpoints():
    """
    通过ETCD_ADDRESSES环境变量，获得etcd服务器的地址。默认情况下，ETCD_ADDRESSES的值为etcd:2379
    :return: [ "http://192.168.100.2:1234", "http://192.168.100.3:2345" ]
    """
    import os

    def get_endpoint(addr):
        """
        根据addr，从其中获得("192.168.100.1", 2345)

        :param addr: 格式：192.168.100.1:2345
        """
        return 'http://%s' % addr

    addresses = filter(bool, os.getenv('ETCD_ADDRESSES', 'etcd:2379').split(','))
    return map(get_endpoint, addresses)


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
    urls = ['%s/v2/keys/backends/%s' % (etcd_addr, service_name) for etcd_addr in get_etcd_endpoints()]

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
        nodes = request(urls)['node']['nodes']
        return {alias: dict(map(get_service_entry, nodes))}
    except (KeyError, IndexError, ValueError):
        return None


def build_conf(node, alias=None):
    """
    获得配置信息

    :param node:
    :param alias:
    :return:
    """
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


def request(url_list):
    """
    根据url_list，依次发送HTTP请求，并返回相应的JSON响应。如果一个请求失败，则进行下一个。如果全部失败，则抛出最后的异常。
    :param url_list:
    :return:
    """
    last_exception = ValueError('url_list is empty')

    for url in url_list:
        try:
            return requests.get(url).json()
        except (ValueError, RequestException) as e:
            last_exception = e
            continue

    raise last_exception


def get_config(service_names=None, conf_names=None, cache_key=None, force_refresh=False):
    """
    给定服务键名和配置键名，获得所有的配置信息
    :param service_names: 服务列表。具有两种形式。1. 指定键名：[ "rabbitmq", "mongodb" ]。
    2. 指定键名和别名：[ ("rabbitmq-node1", "rabbitmq"), ("mongodb-master", "mongodb") ]。这两种形式可以混合使用。
    :param conf_names: 配置信息列表。和服务列表类似，也具有具有别名和不具有别名这两种形式。
    :param cache_key: 如果指定了cache_key：取得的数据会被缓存，同时今后也可以根据cache_key取出
    :param force_refresh: 强制刷新缓存
    :return:
    """
    if not force_refresh and cache_key and cache_key in cached_conf_map:
        return cached_conf_map[cache_key]

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
        urls = ['%s/v2/keys/project-conf/%s?recursive=true' % (etcd_url, name) for etcd_url in get_etcd_endpoints()]
        data = request(urls)
        if 'node' not in data:
            continue
        else:
            conf_map.update(build_conf(data['node'], alias=alias))

    from apiumworker.global_conf import parse_cl_args

    project_conf, _ = parse_cl_args()

    config = merge_dicts({'services': services}, conf_map, project_conf)

    if cache_key:
        cached_conf_map[cache_key] = config

    return config

