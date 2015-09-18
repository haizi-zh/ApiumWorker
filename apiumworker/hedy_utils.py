# coding=utf-8
import json

from apiumworker import get_config


__author__ = 'zephyre'

# 处理和IM相关的事务

class MessageType:
    # 文本消息
    TEXT = 0

    # 语音消息
    AUDIO = 1

    # 图像消息
    IMAGE = 2

    # 位置消息
    LOCATION = 3

    # 目的地消息
    LOCALITY = 11

    # 游记消息
    TRAVELNOTE = 12

    # 景点消息
    VIEWSPOT = 13

    # 餐厅消息
    RESTAURANT = 14

    # 购物消息
    SHOPPING = 15

    # 酒店消息
    HOTEL = 16


class ChatType:
    # 单聊
    SINGLE = 'single'

    # 群聊
    CHATGROUP = 'group'


def _build_message(sender, receiver, contents, msg_type, chat_type):
    """
    私有方法。在构造好contents之后，通过此方法，可以构造出最终的消息体
    :param sender: 发送者ID
    :param receiver: 接收者ID
    :param contents: 消息内容
    :param msg_type: 消息类型
    :param chat_type: 聊天类型（单聊/群聊)
    :return:
    """
    # contents有两种情况：纯文本，或dict。需要分别处理，最终得到字符串类型的contents，形成message
    contents = contents if isinstance(contents, basestring) else json.dumps(contents)
    return {
        'msgType': msg_type,
        'chatType': chat_type,
        'contents': contents,
        'receiver': receiver,
        'sender': sender
    }


def build_text_message(sender, receiver, text, chat_type=ChatType.SINGLE):
    """
    构造纯文本消息
    :param sender: 发送者ID
    :param receiver: 接收者ID
    :param contents: 消息内容
    """
    return _build_message(sender, receiver, text, MessageType.TEXT, chat_type)


def build_locality_message(sender, receiver, loc_id, name, image=None, chat_type=ChatType.SINGLE, **kwargs):
    """
    构造目的地消息
    :param sender: 发送者ID
    :param receiver: 接收者ID
    :param loc_id: 目的地ID
    :param name: 目的地名称
    :param kwargs: 目的地的其它属性。包括：desc: 目的地描述
    """
    loc_data = {
        'id': loc_id,
        'name': name,
        'image': image if image else '',
        'desc': kwargs.get('desc', '')
    }
    return _build_message(sender, receiver, loc_data, MessageType.LOCALITY, chat_type)


def build_viewspot_message(sender, receiver, vs_id, name, image=None, chat_type=ChatType.SINGLE, **kwargs):
    """
    构造景点消息
    :param sender: 发送者ID
    :param receiver: 接收者ID
    :param vs_id: 景点ID
    :param name: 景点名称
    :param kwargs: 景点的其它属性。包括：timeCost: 游玩时间，desc: 景点描述
    """
    vs_data = {
        'id': vs_id,
        'name': name,
        'image': image if image else '',
        'desc': kwargs.get('desc', '')
    }
    return _build_message(sender, receiver, vs_data, MessageType.VIEWSPOT, chat_type)


def build_travelnote_message(sender, receiver, note_id, url, name, image=None, chat_type=ChatType.SINGLE, **kwargs):
    """
    构造游记消息
    :param sender: 发送者ID
    :param receiver: 接收者ID
    :param node_id: 游记ID
    :param url: 游记的链接
    :param name: 游记标题
    :param kwargs: 游记的其它属性。包括：desc: 游记描述
    """
    note_data = {
        'id': note_id,
        'name': name,
        'image': image if image else '',
        'detailUrl': url,
        'desc': kwargs.get('desc', '')
    }
    return _build_message(sender, receiver, note_data, MessageType.VIEWSPOT, chat_type)


def send_message(message):
    """
    发送消息
    :param message: 消息
    :return:
    """
    import requests

    hedy_host = get_config(service_names=['hedy'], cache_key='hedy')['services']['hedy'].values()[0]['host']
    hedy_port = int(get_config(service_names=['hedy'], cache_key='hedy')['services']['hedy'].values()[0]['port'])

    server_addr = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    headers = {'Content-Type': 'application/json'}

    requests.post(server_addr, data=json.dumps(message), headers=headers)
