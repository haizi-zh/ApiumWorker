__author__ = 'zephyre'

from kombu import Exchange, Queue

CELERY_ACCEPT_CONTENT = ['json']

CELERY_QUEUES = (
    Queue('contact.createUser.contact', Exchange('contact.createUser', type='fanout')),
    Queue('contact.login.contact', Exchange('contact.login', type='fanout')),
    Queue('contact.resetPassword.contact', Exchange('contact.resetPassword', type='fanout')),
    Queue('contact.addContacts.contact', Exchange('contact.addContacts', type='fanout')),
    Queue('contact.removeContacts.contact', Exchange('contact.removeContacts', type='fanout')),
    Queue('contact.modUserInfo.contact', Exchange('contact.modUserInfo', type='fanout')),
    Queue('contact.createChatGroup.contact', Exchange('contact.createChatGroup', type='fanout')),
    Queue('contact.addGroupMembers.contact', Exchange('contact.addGroupMembers', type='fanout')),
    Queue('contact.removeGroupMembers.contact', Exchange('contact.removeGroupMembers', type='fanout')),
    Queue('contact.modChatGroup.contact', Exchange('contact.modChatGroup', type='fanout')),
    Queue('contact.sendContactRequest.contact', Exchange('contact.sendContactRequest', type='fanout')),
    Queue('contact.acceptContactRequest.contact', Exchange('contact.acceptContactRequest', type='fanout')),
    Queue('contact.rejectContactRequest.contact', Exchange('contact.rejectContactRequest', type='fanout')),
)
