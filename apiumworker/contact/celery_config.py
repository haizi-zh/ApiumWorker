__author__ = 'zephyre'

from kombu import Exchange, Queue

CELERY_ACCEPT_CONTENT = ['json']

CELERY_QUEUES = (
    Queue('yunkai.createUser.contact', Exchange('yunkai.createUser', type='fanout')),
    Queue('yunkai.login.contact', Exchange('yunkai.login', type='fanout')),
    # Queue('yunkai.resetPassword.contact', Exchange('yunkai.resetPassword', type='fanout')),
    # Queue('yunkai.addContacts.contact', Exchange('yunkai.addContacts', type='fanout')),
    # Queue('yunkai.removeContacts.contact', Exchange('yunkai.removeContacts', type='fanout')),
    # Queue('yunkai.modUserInfo.contact', Exchange('yunkai.modUserInfo', type='fanout')),
    # Queue('yunkai.createChatGroup.contact', Exchange('yunkai.createChatGroup', type='fanout')),
    Queue('yunkai.addGroupMembers.contact', Exchange('yunkai.addGroupMembers', type='fanout')),
    Queue('yunkai.removeGroupMembers.contact', Exchange('yunkai.removeGroupMembers', type='fanout')),
    # Queue('yunkai.modChatGroup.contact', Exchange('yunkai.modChatGroup', type='fanout')),
    Queue('yunkai.sendContactRequest.contact', Exchange('yunkai.sendContactRequest', type='fanout')),
    Queue('yunkai.acceptContactRequest.contact', Exchange('yunkai.acceptContactRequest', type='fanout')),
    # Queue('yunkai.rejectContactRequest.contact', Exchange('yunkai.rejectContactRequest', type='fanout')),
)
