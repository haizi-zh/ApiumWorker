__author__ = 'zephyre'

from kombu import Exchange, Queue

CELERY_ACCEPT_CONTENT = ['json']

CELERY_QUEUES = (
    Queue('hedylogos.filterMessage.default', Exchange('hedylogos.filterMessage', type='fanout')),
)
