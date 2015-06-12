__author__ = 'zephyre'


def __init_app():
    from celery import Celery
    from apiumworker.etcd_conf import get_config

    conf = get_config(['smscenter', 'rabbitmq'], ['smscenter', 'rabbitmq'])

    from apiumworker.sms import celery_config

    conf_rabbitmq = conf['conf']['smscenter']['rabbitmq']
    service_rabbitmq = conf['services']['rabbitmq']
    the_app = Celery('ApiumWorker', broker='amqp://%s:%s@%s:%d/%s' %
                                           (conf_rabbitmq['username'], conf_rabbitmq['password'],
                                            service_rabbitmq['host'], service_rabbitmq['port'],
                                            conf_rabbitmq['virtualhost']))
    the_app.config_from_object(celery_config)

    return the_app


app = __init_app()

