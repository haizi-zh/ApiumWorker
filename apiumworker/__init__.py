# coding=utf-8

from celery import Celery

from apiumworker.etcd_conf import get_config

__author__ = 'zephyre'


def init_celery_app(amqp_conf):
    """
    创建Celery app对象
    :param amqp_conf: AMQP配置。其中包括：username, password, host, port以及virtualhost设置
    :return: Celery app对象
    """
    from apiumworker.contact import celery_config

    username = amqp_conf.get('username')
    password = amqp_conf.get('password')
    host = amqp_conf.get('host', 'localhost')
    port = amqp_conf.get('port', 5672)
    virtualhost = amqp_conf.get('virtualhost', '/')

    if username and password:
        amqp_uri = 'amqp://%s:%s@%s:%d/%s' % (username, password, host, port, virtualhost)
    else:
        amqp_uri = 'amqp://%s:%d/%s' % (host, port, virtualhost)

    the_app = Celery('ApiumWorker', broker=amqp_uri)
    the_app.config_from_object(celery_config)

    return the_app



