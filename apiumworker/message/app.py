# coding=utf-8
__author__ = 'zephyre'


def _init():
    import os
    from apiumworker.etcd_conf import get_config
    from apiumworker import init_celery_app

    # 通过环境变量APIUMWORKER_RUN_LEVEL获得运行模式。默认情况下为dev。
    runlevel = os.getenv('APIUMWORKER_RUN_LEVEL', 'dev')

    if runlevel == 'production':
        apiumworker_name = 'apiumworker'
    elif runlevel == 'dev':
        apiumworker_name = 'apiumworker-dev'
    else:
        assert False

    # 获得服务列表
    if runlevel == 'production':
        services = ['rabbitmq', 'hedy']
    elif runlevel == 'dev':
        services = ['rabbitmq', ('hedy-dev', 'hedy')]
    else:
        assert False

    conf = get_config(services, [(apiumworker_name, 'apiumworker')],
                      cache_key='apiumworker.contact')

    rabbitmq_entries = conf['services']['rabbitmq'].values()

    amqp_conf = conf['apiumworker']['rabbitmq']
    amqp_conf['host'] = rabbitmq_entries[0]['host']
    amqp_conf['port'] = rabbitmq_entries[0]['port']

    the_app = init_celery_app(amqp_conf)

    from apiumworker.message import celery_config

    the_app.config_from_object(celery_config)

    return the_app


app = _init()