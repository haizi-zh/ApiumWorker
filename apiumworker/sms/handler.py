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
    # test = json.dumps(user)
    # userInfo = json.loads(test)
    logger.info('%d %s %s' % (user['userId'], user['nickName'], source))
    url = 'http://hedy.zephyre.me/chats'  # hedylogos发消息接口
    data = {
        'chatType': 'single',
        'contents': 'welcome %s login' % user['nickName'],
        'msgType': 0,
        'receiver': user,
        'sender': {'userId': 100000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户修改信息事件
@app.task(serializer='json', name='yunkai.onModUserInfo')
def update_userinfo_handler(user, miscInfo):
    logger.info('%d %s' % (user['userId'], user['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'update user %d info success' % user['userId'],
        'msgType': 0,
        'receiver': user,
        'sender': {'userId': 100000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 发送好友请求事件
@app.task(serializer='json', name='yunkai.onSendContactRequest')
def send_contact_request_handler(requestId, message, sender, receiver, miscInfo):
    logger.info('requestId = %s , message = %s' % (requestId, message))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'requestId': requestId,
        'contents': '%s请求添加好友, 附言:%s' % (sender['nickName'], message),
        'msgType': 0,
        'receiver': receiver,
        'sender': sender
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 接受好友请求事件
@app.task(serializer='json', name='yunkai.onAcceptContactRequest')
def accept_contact_request_handler(requestId, sender, receiver, miscInfo):
    logger.info('requestId = %s' % requestId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'requestId': requestId,
        'contents': '%s 接受了您的好友请求' % sender['nickName'],
        'msgType': 0,
        'receiver': receiver,
        'sender': sender
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 拒绝好友请求事件
@app.task(serializer='json', name='yunkai.onRejectContactRequest')
def reject_contact_request_handler(requestId, message, sender, receiver, miscInfo):
    logger.info('%s' % requestId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'requestId': requestId,
        'contents': '%s 拒绝了您的好友请求, 附言: %s' % (sender['nickName'], message),
        'msgType': 0,
        'receiver': receiver,
        'sender': sender
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 添加联系人事件，A添加B
@app.task(serializer='json', name='yunkai.onAddContacts')
def add_contacts_handler(user, targets, miscInfo):
    logger.info('%s and %s be friends' % (user['nickName'], targets['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s and %s be friends' % (user['nickName'], targets['nickName']),
        'msgType': 0,
        'receiver': targets,
        'sender': user
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除联系人事件，A删除B
@app.task(serializer='json', name='yunkai.onRemoveContacts')
def remove_contacts_handler(user, targets, miscInfo):
    logger.info('%s and %s be not friends' % (user['nickName'], targets['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s and %s be not friends' % (user['nickName'], targets['nickName']),
        'msgType': 0,
        'receiver': targets,
        'sender': user
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
        'contents': '%s reset password success!' % user['nickName'],
        'msgType': 0,
        'receiver': user,
        'sender': {'userId': 100000, 'nickName': '派派'}
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
        'contents': '%s, congratulations to you be a lvxingpai member' % user['nickName'],
        'msgType': 0,
        'receiver': user,
        'sender': {'userId': 100000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 创建群组事件
@app.task(serializer='json', name='yunkai.onCreateChatGroup')
def create_chatgroup_handler(chatGroup, creator, participants, miscInfo):
    logger.info('%s create chat group %s success' % (creator['nickName'], chatGroup['name']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s create chat group %s success' % (creator['nickName'], chatGroup['name']),
        'msgType': 0,
        'receiver': participants,
        'sender': {'userId': 100000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 修改群组信息事件
@app.task(serializer='json', name='yunkai.onModChatGroup')
def update_chatgroup_handler(chatGroupId, miscInfo):
    logger.info('chatGroup %d be updated' % (chatGroupId))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'chatGroup %d be updated' % (chatGroupId),
        'msgType': 0,
        'receiver': 100068,
        'sender': {'userId': 100000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 添加讨论组成员事件
@app.task(serializer='json', name='yunkai.onAddGroupMembers')
def add_chatgroup_members_handler(chatGroup, operator, targets,
                                  miscInfo):  # chatGroup包含chatGroupId,name,avatar,participants
    logger.info('%s 在 %s 添加了成员' % (operator['nickName'], chatGroup['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s 在 %s 添加了成员' % (operator['nickName'], chatGroup['nickName']),
        'msgType': 0,
        'receiver': targets,
        'sender': operator
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除讨论组成员事件
@app.task(serializer='json', name='yunkai.onRemoveGroupMembers')
def remove_chatgroup_members_handler(chatGroup, operator, targets, miscInfo):
    logger.info('%s 在 %s 添加了成员' % (operator['nickName'], chatGroup['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s 在 %s 删除了成员' % (operator['nickName'], chatGroup['nickName']),
        'msgType': 0,
        'receiver': targets,
        'sender': operator
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)
