__author__ = 'zephyre'

from kombu import Exchange, Queue

CELERY_ACCEPT_CONTENT = ['json']

CELERY_QUEUES = (
    Queue('contact.createUser.sms', Exchange('contact.createUser', type='fanout')),
    Queue('contact.login.sms', Exchange('contact.login', type='fanout')),
    Queue('contact.resetPassword.sms', Exchange('contact.resetPassword', type='fanout')),
    Queue('contact.addContacts.sms', Exchange('contact.addContacts', type='fanout')),
    Queue('contact.removeContacts.sms', Exchange('contact.removeContacts', type='fanout')),
    Queue('contact.modUserInfo.sms', Exchange('contact.modUserInfo', type='fanout')),
    Queue('contact.createChatGroup.sms', Exchange('contact.createChatGroup', type='fanout')),
    Queue('contact.addGroupMembers.sms', Exchange('contact.addGroupMembers', type='fanout')),
    Queue('contact.removeGroupMembers.sms', Exchange('contact.removeGroupMembers', type='fanout')),
    Queue('contact.modChatGroup.sms', Exchange('contact.modChatGroup', type='fanout')),
    Queue('contact.sendContactRequest.sms', Exchange('contact.sendContactRequest', type='fanout')),
    Queue('contact.acceptContactRequest.sms', Exchange('contact.acceptContactRequest', type='fanout')),
    Queue('contact.rejectContactRequest.sms', Exchange('contact.rejectContactRequest', type='fanout')),
)
