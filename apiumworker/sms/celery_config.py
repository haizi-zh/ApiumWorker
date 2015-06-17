__author__ = 'zephyre'

from kombu import Exchange, Queue


CELERY_ACCEPT_CONTENT = ['json']


CELERY_QUEUES = (
    Queue('yunkai.login.sms', Exchange('yunkai.login', type='fanout')),
    # Queue('yunkai.login.im', Exchange('yunkai.login', type='fanout'))
)

