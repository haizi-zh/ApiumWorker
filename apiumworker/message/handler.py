# coding=utf-8
__author__ = 'zephyre'

import re
import json

from qiniu import Auth
from celery.utils.log import get_task_logger
import requests

from apiumworker.message.app import app
from apiumworker.etcd_conf import get_config


logger = get_task_logger('apium')

USERID_PAIPAI = 10000
USERID_WENWEN = 10001

hedy_host = get_config(cache_key='apiumworker.contact')['services']['hedy'].values()[0]['host']
hedy_port = get_config(cache_key='apiumworker.contact')['services']['hedy'].values()[0]['port']

qiniu_client = Auth('jU6KkDZdGYODmrPVh5sbBIkJX65y-Cea991uWpWZ', 'OVSfoBU_Lzb6QgMWCvOD0x1mDO10JxIOwCuIYNr0')

# 接收到消息的事件
@app.task(serializer='json', name='hedylogos.onFilterMessage')
def filter_message_handler(**kwargs):
    """
    接收到消息的处理函数。
    :return:
    """
    receiver = kwargs['receiverId']

    if receiver == USERID_PAIPAI:
        # 这是发送给派派的消息
        paipai_filter(**kwargs)
    elif receiver == USERID_WENWEN:
        wenwen_filter(**kwargs)


def _build_text_message(sender_id, receiver_id, text):
    """
    发送纯文本消息
    :param sender_id:
    :param receiver_id:
    :param text:
    :return:
    """
    return {
        'msgType': 0,
        'chatType': 'single',
        'contents': text,
        'receiver': receiver_id,
        'sender': sender_id
    }


def _build_image_message(sender_id, receiver_id, **kwargs):
    """
    发送图像消息
    :param sender_id:
    :param receiver_id:
    :param text:
    :return:
    """

    key = kwargs['key']
    bucket_domain = kwargs['bucket_domain']
    base_url = 'http://%s/%s' % (bucket_domain, key)

    style = ['thumb', 'full']

    # 默认一周以后过期
    expires = 7 * 24 * 3600

    private_urls = {tmp: qiniu_client.private_download_url('%s!%s' % (base_url, tmp), expires=expires) for tmp in style}

    contents = {'width': kwargs['width'], 'height': kwargs['height']}
    for k, v in private_urls.items():
        contents[k] = v

    return {'msgType': 2, 'chatType': 'single', 'contents': json.dumps(contents),
            'receiver': receiver_id, 'sender': sender_id}


def _send_message(message):
    """
    发送一条单聊消息
    :param message:
    :return:
    """
    server_addr = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    headers = {'Content-Type': 'application/json'}
    requests.post(server_addr, data=json.dumps(message), headers=headers)


def etcd_request(key, method='GET', **kwargs):
    """
    请求etcd数据库
    :param key:
    :param method:
    :param kwargs:
    :return:
    """
    from apiumworker.etcd_conf import request, get_etcd_endpoints

    from urlparse import urljoin

    url_list = [urljoin(tmp, '/v2/keys%s' % key) for tmp in get_etcd_endpoints()]

    return request(url_list, method, **kwargs)


def paipai_filter(**kwargs):
    """
    处理派派收到的消息
    :return:
    """
    sender = kwargs['senderId']
    chat_type = kwargs['chatType']
    msg_type = kwargs['msgType']
    contents = kwargs['contents'].strip()

    def jd_lottery(tel):
        logger.info(u'Lottery registered for %d: %s' % (sender, tel))

        # 注册到etcd服务器中。默认30天过期
        ttl = 30 * 24 * 3600
        key = '/lottery20150826/%d?ttl=%d' % (sender, ttl)
        r = etcd_request(key, method='PUT', data={'value': tel})
        logger.debug(r)

        new_contents = u'亲爱的，已经收到您参与活动的信息了，派派会在活动结束后3个工作日内通知您中奖结果，' \
                       u'中奖名单也会在旅行派官方微博中公布，敬请期待哟~么么哒~'
        msg = _build_text_message(USERID_PAIPAI, sender, new_contents)
        _send_message(msg)

    def letv_qr_code():
        msg1 = _build_text_message(USERID_PAIPAI, sender, u'乐视永久会员二维码送上，么么哒~')
        _send_message(msg1)

        key = '31434498-7d4d-4fb5-b7b4-757e01efd5f1'
        bucket_domain = '7xirnn.com1.z0.glb.clouddn.com'
        msg2 = _build_image_message(USERID_PAIPAI, sender, key=key, bucket_domain=bucket_domain, width=160, height=160)
        _send_message(msg2)

    if chat_type == 'single' and msg_type == 0:
        m = re.search(ur'^我要京东卡.*(1\d{10})', contents)
        if m:
            jd_lottery(m.group(1))
        elif contents.strip() == u'我要码' and sender == 100056:
            letv_qr_code()


def wenwen_filter(**kwargs):
    """
    处理问问收到的消息
    :return:
    """
    sender = kwargs['senderId']
    chat_type = kwargs['chatType']

    if chat_type == 'single':
        # contents = u'亲，欢迎使用旅行问问功能，好吧，我是个机器人，不过目前这个版本我还在完善中，敬请期待下个版本的我。'

        contents = u'亲爱的，我是问问，你的旅行贴心小助手。今后，你若是有任何旅行方面的问题，随时都可以来和我讨论。不过呢，我现在还' \
                   u'正在旅行大学里读书充电呢。所以，还请耐心一点点，稍等一小会儿，待我毕业以后就来陪你~'
        msg = _build_text_message(USERID_WENWEN, sender, contents)
        _send_message(msg)
