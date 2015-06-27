# coding=utf-8
import json

__author__ = 'zephyre'

from celery.utils.log import get_task_logger
from apiumworker.sms.app import app
import requests

logger = get_task_logger('apium')


# 登录事件
@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(*args, **kwargs):
    user_id = kwargs['id']
    nick_name = kwargs['nickName']
    logger.info('%d: %s' % (user_id, nick_name))
    url = 'http://hedy.zephyre.me/chats'  # hedylogos发消息接口
    data = {
        'chatType': 'single',
        'contents': 'welcome %s login' % nick_name,
        'msgType': 0,
        'receiver': {'userId': 100068, 'nickName': nick_name},
        'sender': {'userId': 100000}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户修改信息事件
@app.task(serializer='json', name='yunkai.onModUserInfo')
def update_userinfo_handler(userId, nickName, avatar):
    logger.info('%d: %s' % (userId, nickName))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'update user info success',
        'msgType': 0,
        'receiver': userId,
        'sender': 10000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 添加联系人事件，A添加B
@app.task(serializer='json', name='yunkai.onAddContacts')
def add_contacts_handler(userA, nickNameA, avatarA, userB, nickNameB, avatarB):
    logger.info('%d %s %s %d %s %s' % (userA, nickNameA, avatarA, userB, nickNameB, avatarB))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'You are friends with %s' % nickNameB,
        'msgType': 0,
        'receiver': {'userId': userB, 'nickName': nickNameA, 'avatar': avatarA},
        'sender': {'userId': 10000, 'nickName': nickNameB, 'avatar': avatarB}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除联系人事件，A删除B
@app.task(serializer='json', name='yunkai.onRemoveContacts')
def remove_contacts_handler(userA, nickNameA, avatarA, userB, nickNameB, avatarB):
    logger.info('%d %s %s %d %s %s' % (userA, nickNameA, avatarA, userB, nickNameB, avatarB))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'remove friends suceess!',
        'msgType': 0,
        'receiver': {'userId': 100068, 'nickName': nickNameA, 'avatar': avatarA},
        'sender': {'userId': 10000, 'nickName': nickNameB, 'avatar': avatarB}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户密码修改事件
@app.task(serializer='json', name='yunkai.onResetPassword')
def reset_password_handler(userId, nickName, avatar):
    logger.info('%d %s %s' % (userId, nickName, avatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'reset password success!',
        'msgType': 0,
        'receiver': userId,
        'sender': 10000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户注册事件
@app.task(serializer='json', name='yunkai.onCreateUser')
def create_user_handler(*args, **kwargs):
    user_id = kwargs['id']
    nick_name = kwargs['nickName']
    avatar = kwargs['avatar']
    # misc_info = kwargs['miscInfo']
    logger.info('%d: %s %s' % (user_id, nick_name, avatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': u'congratulations to you be a ',
        'msgType': 0,
        'receiver': user_id,
        'sender': 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 创建群组事件
@app.task(serializer='json', name='yunkai.onCreateChatGroup')
def create_chatgroup_handler(chatGroupId, name, avatar, admin, participants):
    logger.info('%d: %s' % (chatGroupId, name))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': 'Create chat group %d success' % chatGroupId,
        'msgType': 0,
        'receiver': 100068,
        'sender': 100053
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 修改群组信息事件
@app.task(serializer='json', name='yunkai.onModChatGroup')
def update_chatgroup_handler(chatGroupId, filed):
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
def add_chatgroup_members_handler(chatGroupId, participants, userInfos):
    logger.info('%d' % chatGroupId)
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
def remove_chatgroup_members_handler(chatGroupId, participants, userInfos):
    logger.info('%d' % chatGroupId)
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
