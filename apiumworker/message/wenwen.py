# coding=utf-8
import json

__author__ = 'zephyre'

from apiumworker.thrift_utils import init_client
from apiumworker.message.semat import SemaProcessor

semat_host = '192.168.100.2'
semat_port = 9588

semat_client = init_client(semat_host, semat_port, SemaProcessor)


def get_semantics(message):
    semantics = json.loads(semat_client.understand(message))
    if 'service' in semantics:
        service = semantics['service']
        if service==u'景点':
            proc_viewspots(semantics['semantic'])
        elif service ==u'餐厅':
            proc_restaurants(semantics['semantic'])


def proc_viewspots(semantics):
    """
    处理关于景点的推荐问题
    :param semantics:
    :return:
    """
    pass


def proc_restaurants(semantics):
    """
    处理关于餐厅的推荐问题
    :param semantics:
    :return:
    """
    pass
