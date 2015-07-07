# coding=utf-8
import json

__author__ = 'zephyre'

from celery.utils.log import get_task_logger
from apiumworker.contact.app import app
from apiumworker.etcd_conf import get_config, project_conf

import requests

logger = get_task_logger('apium')

hedy_host = get_config(cache_key='contact')['services']['hedy'].values()[0]['host']
hedy_port = get_config(cache_key='contact')['services']['hedy'].values()[0]['port']


# 登录事件
@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(**kwargs):
    user = kwargs['user']
    source = kwargs['source']

    # test = json.dumps(user)
    # userInfo = json.loads(test)
    logger.info('%d %s %s' % (user['userId'], user['nickName'], source))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')  # hedylogos发消息接口
    welcome = u'欢迎回来'
    headers = {'Content-Type': 'application/json'}

    data = {
        'chatType': 'single',
        'contents': welcome,
        'msgType': 0,
        'receiver': user['userId'],  # user,
        'sender': 100015 #{'userId': 100015, 'nickName': '派派'}
    }

    requests.post(url, data=json.dumps(data), headers=headers)


# 用户修改信息事件
# @app.task(serializer='json', name='yunkai.onModUserInfo')
def update_userinfo_handler(**kwargs):
    user = kwargs['user']
    logger.info('%d %s' % (user['userId'], user['nickName']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    data = {
        'chatType': 'single',
        'contents': 'update user %d info success' % user['userId'],
        'msgType': 0,
        'receiver': user['userId'],  # user,
        'sender': 10000  # {'userId': 10000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


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
    cmd = {
        'chatType': 'single',
        'msgType': 100,
        'contents': {
            "action": "F_ADD",
            "userId": sender['userId'],
            "nickName": sender['nickName'],
            "avatar": sender['avatar'],
            "requestId": request_id,
            "message": message
        }
        # 'receiver': receiver['userId'],
        # 'sender': 0
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
    cmd = {
        'chatType': 'single',
        'msgType': 100,
        'contents': {
            "action": "F_AGREE",
            "userId": receiver['userId'],
            "nickName": receiver['nickName'],
            "avatar": receiver['avatar'],
            "requestId": request_id
        }
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
        'msgType': 100,
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
        'msgType': 0,
        'receiver': user['userId'],  # targets,
        'sender': target['userId']  # user
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

    # user = kwargs['user']
    #
    # url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    # create_user_message_1 = "您好，我是热爱旅行,行迹八方的派派。\r\n在这儿，没有规则，没有底限，随心所欲，畅所欲言。" \
    #                         "欢迎7×24小时的调戏。\r\n世界这么大，约吗？"
    # # create_user_message_2 = "您好"
    #
    # # 添加服务号为好友
    # # addServerContant = client.addContact(user['userId'], 100015)
    #
    # headers = {'Content-Type': 'application/json'}
    # requests.post(url, data=json.dumps(create_user_message_1), headers=headers)
    # # requests.post(url, data=json.dumps(create_user_message_2), headers=headers)
    # # 将服务号添加为好友


# 创建群组事件
# @app.task(serializer='json', name='yunkai.onCreateChatGroup')
def create_chatgroup_handler(**kwargs):
    chat_group = kwargs['chatGroup']
    creator = kwargs['creator']

    logger.info('%s create chat group %s success' % (creator['nickName'], chat_group['name']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    data = {
        'chatType': 'single',
        'contents': '%s create chat group %s success' % (creator['nickName'], chat_group['name']),
        'msgType': 0,
        'receiver': creator['userId'],  # participants,
        'sender': 10000  # {'userId': 10000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 修改群组信息事件
# @app.task(serializer='json', name='yunkai.onModChatGroup')
def update_chatgroup_handler(**kwargs):
    chat_group = kwargs['chatGroup']
    operator = kwargs['operator']

    logger.info('chatGroup %d be updated' % (chat_group['chatGroupId']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    tips = {
        'msgType': 200,
        'operator': {
            'userId': operator['userId'],
            'nickName': operator['nickName']
        },
        'contents': {
            'tipType': 2003,
            'name': chat_group['name']
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(tips), headers=headers)


# 添加讨论组成员事件
@app.task(serializer='json', name='yunkai.onAddGroupMembers')
def add_chatgroup_members_handler(**kwargs):
    operator = kwargs['operator']
    targets = kwargs['targets']
    chat_group = kwargs['chatGroup']

    logger.info('%s 在 %s 添加了成员' % (operator['nickName'], chat_group['nickName']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')

    tips = {
        'msgType': 200,
        'contents': {
            'tipType': 2001,
            'operator': {
                'userId': operator['userId'],
                'nickName': operator['nickName']
            },
            'targets': [{
                            'userId': targets['userId'],
                            'nickName': targets['nickName']
                        }],
            'chatGroupId': chat_group['chatGroupId']
        }
    }
    headers = {'Content-Type': 'application/json'}
    # requests.post(url, data=json.dumps(cmd), headers=headers)
    requests.post(url, data=json.dumps(tips), headers=headers)


# 删除讨论组成员事件
@app.task(serializer='json', name='yunkai.onRemoveGroupMembers')
def remove_chatgroup_members_handler(**kwargs):
    operator = kwargs['operator']
    chat_group = kwargs['chatGroup']
    targets = kwargs['targets']

    logger.info('%s 在 %s 添加了成员' % (operator['nickName'], chat_group['nickName']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')

    tips = {
        'msgType': 200,
        'contents': {
            'tipType': 2002,
            'operator': {
                'userId': operator['userId'],
                'nickName': operator['nickName']
            },
            'targets': [{
                            'userId': targets['userId'],
                            'nickName': targets['nickName']
                        }],
            'chatGroupId': chat_group['chatGroupId']
        }
    }
    headers = {'Content-Type': 'application/json'}
    # requests.post(url, data=json.dumps(cmd), headers=headers)
    requests.post(url, data=json.dumps(tips), headers=headers)
