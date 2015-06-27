# coding=utf-8
import json

__author__ = 'zephyre'

from celery.utils.log import get_task_logger
from apiumworker.sms.app import app
import requests

logger = get_task_logger('apium')


# 登录事件
@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(user, source, miscInfo):
    logger.info('%s' % source)
    url = 'http://hedy.zephyre.me/chats'  # hedylogos发消息接口
    data = {
        'chatType': 'single',
        'contents': 'welcome login',
        'msgType': 0,
        'receiver': 100068,#{'userId': 100068, 'nickName': nickName},
        'sender': 100000#{'userId': 100000}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户修改信息事件
@app.task(serializer='json', name='yunkai.onModUserInfo')
def update_userinfo_handler(user, miscInfo):
    logger.info('modify user info')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'update user info success',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 发送好友请求事件
@app.task(serializer='json', name='yunkai.onSendContactRequest')
def send_contact_request_handler(requestId, message, sender, receiver, miscInfo):
    logger.info('%s' % message)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '发送好友请求：%s' % message,
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 接受好友请求事件
@app.task(serializer='json', name='yunkai.onAcceptContactRequest')
def accept_contact_request_handler(requestId, sender, receiver, miscInfo):
    logger.info('onAcceptContactRequest')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '接受了好友请求',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 拒绝好友请求事件
@app.task(serializer='json', name='yunkai.onRejectContactRequest')
def reject_contact_request_handler(requestId, message, sender, receiver, miscInfo):
    logger.info('%s' % message)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '拒绝了好友请求',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)

# 添加联系人事件，A添加B
@app.task(serializer='json', name='yunkai.onAddContacts')
def add_contacts_handler(user, targets, miscInfo):
    logger.info('你们成为好友')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'You are friends！',
        'msgType': 0,
        'receiver': 100068,#{'userId': userB, 'nickName': nickNameA, 'avatar': avatarA},
        'sender': 100000#{'userId': 10000, 'nickName': nickNameB, 'avatar': avatarB}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除联系人事件，A删除B
@app.task(serializer='json', name='yunkai.onRemoveContacts')
def remove_contacts_handler(user, targets, miscInfo):
    logger.info('解除好友关系')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'remove friends suceess!',
        'msgType': 0,
        'receiver': 100068,#{'userId': 100068, 'nickName': nickNameA, 'avatar': avatarA},
        'sender': 100000#{'userId': 10000, 'nickName': nickNameB, 'avatar': avatarB}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户密码修改事件
@app.task(serializer='json', name='yunkai.onResetPassword')
def reset_password_handler(user, miscInfo):
    logger.info('Reset Password')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'reset password success!',
        'msgType': 0,
        'receiver': 1000068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户注册事件
@app.task(serializer='json', name='yunkai.onCreateUser')
def create_user_handler(user, miscInfo):
    logger.info('create user')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'congratulations to you be a lvxingpai member',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 创建群组事件
@app.task(serializer='json', name='yunkai.onCreateChatGroup')
def create_chatgroup_handler(chatGroup, creator, participants, miscInfo):
    logger.info('Create chat group')
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'Create chat group success',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100053
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 修改群组信息事件
@app.task(serializer='json', name='yunkai.onModChatGroup')
def update_chatgroup_handler(chatGroupId, miscInfo):
    logger.info('chatGroupId = %d' % (chatGroupId))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 添加讨论组成员事件
@app.task(serializer='json', name='yunkai.onAddGroupMembers')
def add_chatgroup_members_handler(chatGroup, operator, targets, miscInfo):#chatGroup包含chatGroupId,name,avatar,participants
    # logger.info('%d' % chatGroupId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除讨论组成员事件
@app.task(serializer='json', name='yunkai.onRemoveGroupMembers')
def remove_chatgroup_members_handler(chatGroup, operator, targets, miscInfo):
    # logger.info('%d' % chatGroupId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '',
        'msgType': 0,
        'receiver': 100068,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)
