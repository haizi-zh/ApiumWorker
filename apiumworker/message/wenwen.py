# coding=utf-8
import json

__author__ = 'zephyre'

from apiumworker.thrift_utils import init_client
from apiumworker.message.semat import SemaProcessor

semat_host = '192.168.100.2'
semat_port = 9588

semat_client = init_client(semat_host, semat_port, SemaProcessor)


def process_text_message(text_message):
    """
    处理发送给问问的纯文本消息
    :param text_message: 消息内容
    :return:
    """
    # semantics = get_semantics(text_message['contents'])
    semantics = {}
    if 'service' in semantics:
        service = semantics['service']
        if service == u'景点':
            proc_viewspots(semantics['semantic'])
        elif service == u'餐厅':
            proc_restaurants(semantics['semantic'])
        else:
            pass


def get_semantics(message):
    """
    调用讯飞接口，获得语义理解结果
    :param message:
    :return:
    """
    return json.loads(semat_client.understand(message))



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
