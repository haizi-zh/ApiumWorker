__author__ = 'zephyre'

from kombu import Exchange, Queue


CELERY_ACCEPT_CONTENT = ['json']


CELERY_QUEUES = (
    Queue('yunkai.createUser.sms', Exchange('yunkai.createUser', type='fanout')),
    Queue('yunkai.login.sms', Exchange('yunkai.login', type='fanout')),
    Queue('yunkai.resetPassword.sms', Exchange('yunkai.resetPassword', type='fanout')),
    Queue('yunkai.addContacts.sms', Exchange('yunkai.addContacts', type='fanout')),
    Queue('yunkai.removeContacts.sms', Exchange('yunkai.removeContacts', type='fanout')),
    Queue('yunkai.modUserInfo.sms', Exchange('yunkai.modUserInfo', type='fanout')),
    Queue('yunkai.createChatGroup.sms', Exchange('yunkai.createChatGroup', type='fanout')),
    Queue('yunkai.addGroupMembers.sms', Exchange('yunkai.addGroupMembers', type='fanout')),
    Queue('yunkai.removeGroupMembers.sms', Exchange('yunkai.removeGroupMembers', type='fanout')),
)

