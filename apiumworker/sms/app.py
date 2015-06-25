__author__ = 'zephyre'


def __init_app():
    from celery import Celery
    from apiumworker.etcd_conf import get_config, project_conf

    runlevel = project_conf['runlevel']
    if runlevel == 'production':
        apiumworker_name = 'apiumworker'
    elif runlevel == 'dev':
        apiumworker_name = 'apiumworker-dev'
    elif runlevel == 'test':
        apiumworker_name = 'apiumworker-test'
    else:
        raise ValueError

    conf = get_config(['smscenter', 'rabbitmq'], ['smscenter', (apiumworker_name, 'apiumworker')], cache_key='sms')
    conf_rabbitmq = conf['apiumworker']['rabbitmq']
    service_rabbitmq = conf['services']['rabbitmq']

    from apiumworker.sms import celery_config

    the_app = Celery('ApiumWorker', broker='amqp://%s:%s@%s:%d/%s' %
                                           (conf_rabbitmq['username'], conf_rabbitmq['password'],
                                            service_rabbitmq['host'], service_rabbitmq['port'],
                                            conf_rabbitmq['virtualhost']))
    the_app.config_from_object(celery_config)

    return the_app


app = __init_app()

