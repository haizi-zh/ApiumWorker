# coding=utf-8
import json

__author__ = 'zephyre'

from celery.utils.log import get_task_logger
# from apiumworker.sms.app import app
from apiumworker.contact.app import app  #, client
from apiumworker.contact.app import client
import requests

logger = get_task_logger('apium')


# 登录事件
@app.task(serializer='json', name='contact.onLogin')
def login_handler(user, source, miscInfo):
    # test = json.dumps(user)
    # userInfo = json.loads(test)
    logger.info('%d %s %s' % (user['userId'], user['nickName'], source))
    url = 'http://hedy.zephyre.me/chats'  # hedylogos发消息接口
    welcome = '欢迎回来'
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(welcome), headers=headers)


# 用户修改信息事件
@app.task(serializer='json', name='contact.onModUserInfo')
def update_userinfo_handler(user, miscInfo):
    logger.info('%d %s' % (user['userId'], user['nickName']))
    url = 'http://hedy.zephyre.me/chats'
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
@app.task(serializer='json', name='contact.onSendContactRequest')
def send_contact_request_handler(requestId, message, sender, receiver, miscInfo):
    logger.info('requestId = %s , message = %s, sender = %d, receiver = %d' %
                (requestId, message, sender['userId'], receiver['userId']))
    url = 'http://hedy.zephyre.me/chats'
    cmd = {
        'chatType': 'single',
        'msgType': 100,
        'contents': {
            "action": "F_ADD",
            "userId": sender['userId'],
            "nickName": sender['nickName'],
            "avatar": sender['avatar'],
            "requestId": requestId,
            "message": message
        }
        # 'receiver': receiver['userId'],
        # 'sender': 0
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(cmd), headers=headers)


# 接受好友请求事件
@app.task(serializer='json', name='contact.onAcceptContactRequest')
def accept_contact_request_handler(requestId, sender, receiver, miscInfo):
    logger.info('requestId = %s,sender = %d,receiver = %d' % (requestId, sender['userId'], receiver['userId']))
    url = 'http://hedy.zephyre.me/chats'
    cmd = {
        'chatType': 'single',
        'msgType': 100,
        'contents': {
            "action": "F_AGREE",
            "userId": receiver['userId'],
            "nickName": receiver['nickName'],
            "avatar": receiver['avatar'],
            "requestId": requestId
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(cmd), headers=headers)


# 拒绝好友请求事件
@app.task(serializer='json', name='contact.onRejectContactRequest')
def reject_contact_request_handler(requestId, message, sender, receiver, miscInfo):
    logger.info('%s' % requestId)
    url = 'http://hedy.zephyre.me/chats'
    cmd = {
        'chatType': 'single',
        'msgType': 100,
        'contents': {
            "action": "F_REJECT",
            "userId": sender['userId'],
            "nickName": sender['nickName'],
            "avatar": sender['avatar'],
            "requestId": requestId,
            "message": message
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(cmd), headers=headers)


# 添加联系人事件，A添加B
@app.task(serializer='json', name='contact.onAddContacts')
def add_contacts_handler(user, targets, miscInfo):
    logger.info('%d and %d be friends' % (user['userId'], targets['userId']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s and %s be friends' % (user['nickName'], targets['nickName']),
        'msgType': 0,
        'receiver': user['userId'],  # targets,
        'sender': targets['userId']  # user
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 删除联系人事件，A删除B
@app.task(serializer='json', name='contact.onRemoveContacts')
def remove_contacts_handler(user, targets, miscInfo):
    logger.info('%s and %s be not friends' % (user['nickName'], targets['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s and %s be not friends' % (user['nickName'], targets['nickName']),
        'msgType': 0,
        'receiver': targets['userId'],  # targets,
        'sender': user['userId']  # user
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 用户密码修改事件
@app.task(serializer='json', name='contact.onResetPassword')
def reset_password_handler(user, miscInfo):
    logger.info('Reset Password')
    url = 'http://hedy.zephyre.me/chats'
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
@app.task(serializer='json', name='contact.onCreateUser')
def create_user_handler(user, miscInfo):
    logger.info('create user')
    url = 'http://hedy.zephyre.me/chats'
    createUserMessage1 = "您好，我是热爱旅行,行迹八方的派派。\r\n在这儿，没有规则，没有底限，随心所欲，畅所欲言。欢迎7×24小时的调戏。\r\n世界这么大，约吗？"
    createUserMessage2 = "您好"
    # 添加服务号为好友
    addServerContant = client.addContact(user['userId'], 100015)
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(createUserMessage1), headers=headers)
    requests.post(url, data=json.dumps(createUserMessage2), headers=headers)
    # 将服务号添加为好友


# 创建群组事件
@app.task(serializer='json', name='contact.onCreateChatGroup')
def create_chatgroup_handler(chatGroup, creator, participants, miscInfo):
    logger.info('%s create chat group %s success' % (creator['nickName'], chatGroup['name']))
    url = 'http://hedy.zephyre.me/chats'
    data = {
        'chatType': 'single',
        'contents': '%s create chat group %s success' % (creator['nickName'], chatGroup['name']),
        'msgType': 0,
        'receiver': creator['userId'],  # participants,
        'sender': 10000  # {'userId': 10000, 'nickName': '派派'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


# 修改群组信息事件
@app.task(serializer='json', name='contact.onModChatGroup')
def update_chatgroup_handler(chatGroup, operator, miscInfo):
    logger.info('chatGroup %d be updated' % (chatGroup['chatGroupId']))
    url = 'http://hedy.zephyre.me/chats'
    tips = {
        'msgType': 200,
        'operator': {
            'userId': operator['userId'],
            'nickName': operator['nickName']
        },
        'contents': {
            'tipType': 2003,
            'name': chatGroup['name']
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(tips), headers=headers)


# 添加讨论组成员事件
@app.task(serializer='json', name='contact.onAddGroupMembers')
def add_chatgroup_members_handler(chatGroup, operator, targets,
                                  miscInfo):  # chatGroup包含chatGroupId,name,avatar,participants
    logger.info('%s 在 %s 添加了成员' % (operator['nickName'], chatGroup['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    # if (operator['userId'] != targets['userId']):
    #     cmd = {
    #         'chatType': 'single',
    #         'msgType': 100,
    #         'contents': {
    #             'action': 'G_APPLY',
    #             'userId': targets['userId'],
    #             'nickName': targets['nickName'],
    #             'avatar': targets['avatar'],
    #             'chatGroupId': chatGroup['chatGroupId']
    #         }
    #     }
    # else:
    #     cmd = {
    #         'chatType': 'single',
    #         'msgType': 100,
    #         'contents': {
    #             'action': 'G_INVITE',
    #             'userId': targets['userId'],
    #             'nickName': targets['nickName'],
    #             'avatar': targets['avatar'],
    #             'chatGroupId': chatGroup['chatGroupId']
    #         }
    #     }
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
            'chatGroupId': chatGroup['chatGroupId']
        }
    }
    headers = {'Content-Type': 'application/json'}
    # requests.post(url, data=json.dumps(cmd), headers=headers)
    requests.post(url, data=json.dumps(tips), headers=headers)


# 删除讨论组成员事件
@app.task(serializer='json', name='contact.onRemoveGroupMembers')
def remove_chatgroup_members_handler(chatGroup, operator, targets, miscInfo):
    logger.info('%s 在 %s 添加了成员' % (operator['nickName'], chatGroup['nickName']))
    url = 'http://hedy.zephyre.me/chats'
    # if (operator['userId'] == targets['userId']):
    #     cmd = {
    #         'chatType': 'single',
    #         'msgType': 100,
    #         'contents': {
    #             'action': 'G_QUIT',
    #             'userId': targets['userId'],
    #             'nickName': targets['nickName'],
    #             'avatar': targets['avatar'],
    #             'chatGroupId': chatGroup['chatGroupId']
    #         }
    #     }
    # else:
    #     cmd = {
    #         'chatType': 'single',
    #         'msgType': 100,
    #         'contents': {
    #             'action': 'G_REMOVE',
    #             'userId': targets['userId'],
    #             'nickName': targets['nickName'],
    #             'avatar': targets['avatar'],
    #             'chatGroupId': chatGroup['chatGroupId']
    #         }
    #     }
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
            'chatGroupId': chatGroup['chatGroupId']
        }
    }
    headers = {'Content-Type': 'application/json'}
    # requests.post(url, data=json.dumps(cmd), headers=headers)
    requests.post(url, data=json.dumps(tips), headers=headers)
