# coding=utf-8
import json

__author__ = 'zephyre'

from celery.utils.log import get_task_logger
from apiumworker.contact.app import app
from apiumworker.etcd_conf import get_config
from urlparse import urljoin

import requests

logger = get_task_logger('apium')

hedy_host = get_config(cache_key='apiumworker.contact')['services']['hedy'].values()[0]['host']
hedy_port = get_config(cache_key='apiumworker.contact')['services']['hedy'].values()[0]['port']

essay_host = get_config(cache_key='apiumworker.contact')['apiumworker']['essayHost']

# 系统常量

# 服务号ID
systemId = 0
# 普通消息类型
common_msg = 0
# HTML页面卡片消息
card_msg = 18
# cmd消息类型
cmd_msg = 100
# tips消息类型
tips_msg = 200
# 添加讨论组成员tips类型
add_members_tips = 2001
# 删除讨论组成员tips类型
remove_members_tips = 2002
# 修改讨论组信息tips类型
mod_chatgroup_tips = 2003
# 派派
paipai = 10000
wenwen = 10001

def _send_app_intro(receiver_id):
    """
    发送APP简介的消息
    :param receiver_id:
    :return:
    """
    title = u'欢迎亲爱的使用旅行派，有什么问题都可以跟派派说，派派一定会把你服务到满意为止~\n除了派派，我们这儿还有后宫三千旅行达人，天南海北异域风情款款都有，包你满意~\n我们提供的服务包括但不限于：\n达人互动咨询\n景点信息搜搜\n行程一键生成\n更多服务和知(zi)识(shi)，嗷嗷待哺的等着你来解锁哟～'
    href = '/2015080701/index.html'
    url = urljoin(essay_host, href)
    desc = None
    image = 'http://images.taozilvxing.com/lvxingpai_logo_v1.png'
    message = _build_html_message(10000, receiver_id, title, url, desc, image)
    _send_message(message)


def _send_mt_message(receiver_id):
    """
    发送梦婷的HTML页面
    :param receiver_id:
    :return:
    """
    title = u'带上画笔去旅行'
    desc = u'美女画师背着画笔任性游走异国他乡'
    image = 'http://essay.lvxingpai.com/2015090201/staticfs/cover.png'
    href = '/2015090201/index.html'
    url = urljoin(essay_host, href)
    message = _build_html_message(10000, receiver_id, title, url, desc, image)
    _send_message(message)


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


def _build_html_message(sender_id, receiver_id, title, url, desc=None, image=None):
    """
    发送HTML类型的消息
    :param user_id:
    :param url:
    :return:
    """
    contents = {
        'title': title,
        'desc': desc if desc else '',
        'url': url
    }
    if image:
        contents['image'] = image

    return {
        'msgType': card_msg,
        'chatType': 'single',
        'contents': json.dumps(contents),
        'receiver': receiver_id,
        'sender': sender_id
    }


def _send_message(message):
    """
    发送一条单聊消息
    :param message:
    :return:
    """
    server_addr = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    headers = {'Content-Type': 'application/json'}
    requests.post(server_addr, data=json.dumps(message), headers=headers)


# 登录事件
@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(**kwargs):
    logger.info('create user')
    user = kwargs['user']
    if user['userId'] != 100056:
        return

    user_id = user['userId']

    _send_app_intro(user_id)

    text = u'本期旅行达人推荐：梦婷MT，将世界走出自己的模样。'
    _send_message(_build_text_message(10000, user_id, text))

    _send_mt_message(user_id)


# 用户修改信息事件
# @app.task(serializer='json', name='yunkai.onModUserInfo')
def update_userinfo_handler(**kwargs):
    user = kwargs['user']
    logger.info('%d %s' % (user['userId'], user['nickName']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    message = {
        'chatType': 'single',
        'contents': 'update user %d info success' % user['userId'],
        'msgType': 0,
        'receiver': user['userId'],
        'sender': systemId
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(message), headers=headers)


# 发送好友请求事件
@app.task(serializer='json', name='yunkai.onSendContactRequest')
def send_contact_request_handler(**kwargs):
    request_id = kwargs['requestId']
    message = kwargs['message']
    sender = kwargs['sender']
    receiver = kwargs['receiver']

    logger.info('requestId = %s , message = %s, sender = %d, receiver = %d' %
                (request_id, message, sender['userId'], receiver['userId']))

    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    content = {"action": "F_ADD",
               "userId": sender['userId'],
               "nickName": sender['nickName'],
               "avatar": sender['avatar'],
               "requestId": request_id,
               "message": message
    }
    content2Str = json.dumps(content)
    logger.info('**********%s***************' % content2Str)
    cmd = {
        'chatType': 'single',
        'msgType': cmd_msg,
        'contents': '%s' % content2Str,
        'receiver': receiver['userId'],
        'sender': systemId
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(cmd), headers=headers)


# 接受好友请求事件
@app.task(serializer='json', name='yunkai.onAcceptContactRequest')
def accept_contact_request_handler(**kwargs):
    request_id = kwargs['requestId']
    sender = kwargs['sender']
    receiver = kwargs['receiver']

    logger.info('requestId = %s,sender = %d,receiver = %d' % (request_id, sender['userId'], receiver['userId']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    contents = {
        "action": "F_AGREE",
        "userId": receiver['userId'],
        "nickName": receiver['nickName'],
        "avatar": receiver['avatar'],
        "requestId": request_id
    }
    contents2Str = json.dumps(contents)
    cmd = {
        'chatType': 'single',
        'msgType': cmd_msg,
        'contents': '%s' % contents2Str,
        'receiver': sender['userId'],
        'sender': systemId
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(cmd), headers=headers)


# 拒绝好友请求事件
# @app.task(serializer='json', name='yunkai.onRejectContactRequest')
def reject_contact_request_handler(**kwargs):
    request_id = kwargs['requestId']
    sender = kwargs['sender']
    message = kwargs['message']

    logger.info('%s' % request_id)
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    cmd = {
        'chatType': 'single',
        'msgType': cmd_msg,
        'contents': {
            "action": "F_REJECT",
            "userId": sender['userId'],
            "nickName": sender['nickName'],
            "avatar": sender['avatar'],
            "requestId": request_id,
            "message": message
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(cmd), headers=headers)


# 添加联系人事件，A添加B
# @app.task(serializer='json', name='yunkai.onAddContacts')
def add_contacts_handler(**kwargs):
    user = kwargs['user']
    target = kwargs['target']

    logger.info('%d and %d be friends' % (user['userId'], target['userId']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    data = {
        'chatType': 'single',
        'contents': '%s and %s be friends' % (user['nickName'], target['nickName']),
        'msgType': common_msg,
        'receiver': user['userId'],
        'sender': target['userId']
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除联系人事件，A删除B
# @app.task(serializer='json', name='yunkai.onRemoveContacts')
def remove_contacts_handler(**kwargs):
    user = kwargs['user']
    target = kwargs['target']

    logger.info('%s and %s be not friends' % (user['nickName'], target['nickName']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    data = {
        'chatType': 'single',
        'contents': '%s and %s be not friends' % (user['nickName'], target['nickName']),
        'msgType': 0,
        'receiver': target['userId'],  # targets,
        'sender': user['userId']  # user
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户密码修改事件
# @app.task(serializer='json', name='yunkai.onResetPassword')
def reset_password_handler(**kwargs):
    user = kwargs['user']

    logger.info('Reset Password')
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    data = {
        'chatType': 'single',
        'contents': '%s reset password success!' % user['nickName'],
        'msgType': 0,
        'receiver': user['userId'],  # user,
        'sender': 10000  # {'userId': 100000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户注册事件
@app.task(serializer='json', name='yunkai.onCreateUser')
def create_user_handler(**kwargs):
    logger.info('create user')
    user = kwargs['user']

    user_id = user['userId']

   # _send_app_intro(user_id)
    title = u'欢迎亲爱的使用旅行派，有什么问题都可以跟派派说，派派一定会把你服务到满意为止~\n\n除了派派，我们这儿还有后宫三千旅行达人，天南海北异域风情款款都有，包你满意~\n我们提供的服务包括但不限于：\n达人互动咨询\n景点信息搜搜\n行程一键生成\n\n更多服务和知(zi)识(shi)，嗷嗷待哺的等着你来解锁哟～'
    _send_message(_build_text_message(paipai, user_id, title))
    wenwenDefaultMsg = u'旅行攻略可以找我问问'
    _send_message(_build_text_message(wenwen, user_id, wenwenDefaultMsg))
    text = u'本期旅行达人推荐：花二刀，背着画板去旅行的美女画家。'
    _send_message(_build_text_message(paipai, user_id, text))
    _send_mt_message(user_id)

    guide_contents = {
        "guideId": "55d598e2d174911f789ca3cd",
        "action": "fork"
    }
    server_addr = 'http://api.lvxingpai.com/app/users/%d/guides' % user_id
    headers = {'Content-Type': 'application/json'}
    requests.post(server_addr, data=json.dumps(guide_contents), headers=headers)



# 创建群组事件
# @app.task(serializer='json', name='yunkai.onCreateChatGroup')
def create_chatgroup_handler(**kwargs):
    chat_group = kwargs['chatGroup']
    creator = kwargs['creator']

    logger.info('%s create chat group %s success' % (creator['nickName'], chat_group['name']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    tips = {
        'msgType': tips_msg,
        'creator': {
            'userId': creator['userId'],
            'nickName': creator['nickName']
        },
        'contents': {
            'tipType': 2004,
            'name': chat_group['name']
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(tips), headers=headers)


# 修改群组信息事件
# @app.task(serializer='json', name='yunkai.onModChatGroup')
def update_chatgroup_handler(**kwargs):
    chat_group = kwargs['chatGroup']
    operator = kwargs['operator']

    logger.info('chatGroup %d be updated' % (chat_group['chatGroupId']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    tips = {
        'msgType': tips_msg,
        'operator': {
            'userId': operator['userId'],
            'nickName': operator['nickName']
        },
        'contents': {
            'tipType': mod_chatgroup_tips,
            'name': chat_group['name']
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(tips), headers=headers)


# 添加讨论组成员事件
@app.task(serializer='json', name='yunkai.onAddGroupMembers')
def add_chatgroup_members_handler(**kwargs):
    modify_chatgroup_members_handler(True, **kwargs)


# 删除讨论组成员事件
@app.task(serializer='json', name='yunkai.onRemoveGroupMembers')
def remove_chatgroup_members_handler(**kwargs):
    modify_chatgroup_members_handler(False, **kwargs)


def modify_chatgroup_members_handler(adding, **kwargs):
    operator = kwargs['operator']
    chat_group = kwargs['chatGroup']
    targets = kwargs['targets']

    logger.info(u'%s 在 %s %s了成员' % (operator['nickName'], chat_group['name'], u'添加' if adding else u'删除'))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    contents = {
        'tipType': add_members_tips if adding else remove_members_tips,
        'operator': {
            'userId': operator['userId'],
            'nickName': operator['nickName']
        },
        'targets': targets,
        'chatGroupId': chat_group['chatGroupId']
    }
    tips = {
        'chatType': 'group',
        'msgType': tips_msg,
        'contents': '%s' % json.dumps(contents),
        'receiver': chat_group['chatGroupId'],
        'sender': operator['userId']
    }
    headers = {'Content-Type': 'application/json'}
    ret = requests.post(url, data=json.dumps(tips), headers=headers)
    print ret
