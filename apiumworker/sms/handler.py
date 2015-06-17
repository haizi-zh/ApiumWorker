# coding=utf-8
import json

__author__ = 'zephyre'

from celery.utils.log import get_task_logger
from apiumworker.sms.app import app
import requests
logger = get_task_logger('apium')


# 登录事件
@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(nickName, userId, avatar):
    logger.info('%d: %s' % (userId, nickName))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'welcome %s login' % nickName,
        'msgType' : 0,
        'receiver' : 100068,
        'sender' : 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户修改信息事件
@app.task(serializer='json', name='yunkai.onModUserInfo')
def update_userinfo_handler(userId, nickName, avatar):
    logger.info('%d: %s' % (userId, nickName))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'update user info success',
        'msgType' : 0,
        'receiver' : userId,
        'sender' : 10000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)

# 添加联系人事件，A添加B
@app.task(serializer='json', name='yunkai.onAddContacts')
def add_contacts_handler(userA, userB, userBNickName, userBAvatar):
    logger.info('%d %d %s %s' % (userA, userB, userBNickName, userBAvatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'You are friends with %s' % userBNickName,
        'msgType' : 0,
        'receiver' : userA,
        'sender' : userB
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除联系人事件，A删除B
@app.task(serializer='json', name='yunkai.onRemoveContacts')
def remove_contacts_handler(userA, userB, userBNickName, userBAvatar):
    logger.info('%d %d %s %s' % (userA, userB, userBNickName, userBAvatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'remove friends suceess!',
        'msgType' : 0,
        'receiver' : userB,
        'sender' : userA
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户密码修改事件
@app.task(serializer='json', name='yunkai.onResetPassword')
def reset_password_handler(userId):
    logger.info('%d' % userId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'reset password success!',
        'msgType' : 0,
        'receiver' : userId,
        'sender' : 10000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户注册事件
@app.task(serializer='json', name='yunkai.onCreateUser')
def create_user_handler(userId, nickName, avatar):
    logger.info('%d: %s %s' % (userId, nickName, avatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'congratulations to you be a lvxingpai member',
        'msgType' : 0,
        'receiver' : userId,
        'sender' : 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 创建群组事件
@app.task(serializer='json', name='yunkai.onCreateChatGroup')
def create_chatgroup_handler(chatGroupId, name, groupDesc, groupType, avatar, tags, admin, participants, visible):
    logger.info('%d: %s %s' % (chatGroupId, name, avatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : 'Create chat group %d success' % chatGroupId,
        'msgType' : 0,
        'receiver' : 100001,
        'sender' : 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 修改群组信息事件
@app.task(serializer='json', name='yunkai.onModChatGroup')
def update_chatgroup_handler(chatGroupId, name, groupDesc, avatar, tags, admin, visible):
    logger.info('%d: %s %s' % (chatGroupId, name, avatar))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : '',
        'msgType' : 0,
        'receiver' : 100001,
        'sender' : 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 添加讨论组成员事件
@app.task(serializer='json', name='yunkai.onAddGroupMembers')
def create_user_handler(chatGroupId, participants):
    logger.info('%d' % chatGroupId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : '',
        'msgType' : 0,
        'receiver' : 100001,
        'sender' : 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)

# 删除讨论组成员事件
@app.task(serializer='json', name='yunkai.onRemoveGroupMembers')
def create_user_handler(chatGroupId, participants):
    logger.info('%d' % chatGroupId)
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType' : 'single',
        'contents' : '',
        'msgType' : 0,
        'receiver' : 100001,
        'sender' : 100000
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)