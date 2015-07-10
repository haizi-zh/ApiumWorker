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

# 系统常量

# 服务号ID
systemId = 0
# 普通消息类型
common_msg = 0
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

# 登录事件
@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(**kwargs):
    user = kwargs['user']
    source = kwargs['source']

    logger.info('%d %s %s' % (user['userId'], user['nickName'], source))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')  # hedylogos发消息接口
    welcome = u'欢迎回来'
    headers = {'Content-Type': 'application/json'}

    message = {
        'chatType': 'single',
        'contents': welcome,
        'msgType': common_msg,
        'receiver': user['userId'],
        'sender': systemId
    }

    requests.post(url, data=json.dumps(message), headers=headers)


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
    operator = kwargs['operator']
    targets = kwargs['targets']
    chat_group = kwargs['chatGroup']

    logger.info(u'%s 在 %s 添加了成员' % (operator['nickName'], chat_group['name']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    contents = {
            'tipType': add_members_tips,
            'operator': {
                'userId': operator['userId'],
                'nickName': operator['nickName']
            },
            'targets': targets,
            'chatGroupId': chat_group['chatGroupId']
        }
    contents2Str = json.dumps(contents)
    tips = {
        'chatType': 'group',
        'msgType': tips_msg,
        'contents': '%s' % contents2Str,
        'receiver': chat_group['chatGroupId'],
        'sender': operator['userId']
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(tips), headers=headers)


# 删除讨论组成员事件
@app.task(serializer='json', name='yunkai.onRemoveGroupMembers')
def remove_chatgroup_members_handler(**kwargs):
    operator = kwargs['operator']
    chat_group = kwargs['chatGroup']
    targets = kwargs['targets']

    logger.info(u'%s 在 %s 添加了成员' % (operator['nickName'], chat_group['name']))
    url = 'http://%s:%d%s' % (hedy_host, hedy_port, '/chats')
    contents = {
            'tipType': remove_members_tips,
            'operator': {
                'userId': operator['userId'],
                'nickName': operator['nickName']
            },
            'targets': targets,
            'chatGroupId': chat_group['chatGroupId']
        }
    contents2Str = json.dumps(contents)
    tips = {
        'chatType': 'group',
        'msgType': tips_msg,
        'contents': '%s' % contents2Str,
        'receiver': chat_group['chatGroupId'],
        'sender': operator['userId']
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(tips), headers=headers)
