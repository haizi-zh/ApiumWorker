# coding=utf-8
__author__ = 'zephyre'

from celery.utils.log import get_task_logger
from apiumworker.sms.app import app

logger = get_task_logger('apium')


@app.task(serializer='json', name='yunkai.onLogin')
def login_handler(nickName, userId, avatar, tel):
    logger.info('%d: %s, %s' % (userId, nickName, tel))
