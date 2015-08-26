# coding=utf-8
__author__ = 'pengyt'


def _init_thrift_client(host, port):
    """
    创建Thrift client
    :param host: 主机地址
    :param port: 端口
    :return: Thrift client对象
    """
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol
    from apiumworker.contact.users import userservice

    socket = TSocket.TSocket(host, port)
    tranport = TTransport.TFramedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(tranport)
    tranport.open()

    return userservice.Client(protocol)


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
        services = ['yunkai', 'rabbitmq', 'hedy']
    elif runlevel == 'dev':
        services = [('yunkai-dev', 'yunkai'), 'rabbitmq', ('hedy-dev', 'hedy')]
    else:
        assert False

    conf = get_config(services, [(apiumworker_name, 'apiumworker')],
                      cache_key='apiumworker.contact')

    server_entries = conf['services']['yunkai'].values()
    # 默认只使用第一个节点
    host = server_entries[0]['host']
    port = server_entries[0]['port']

    rabbitmq_entries = conf['services']['rabbitmq'].values()

    amqp_conf = conf['apiumworker']['rabbitmq']
    amqp_conf['host'] = rabbitmq_entries[0]['host']
    amqp_conf['port'] = rabbitmq_entries[0]['port']

    thrift_client = _init_thrift_client(host, port)
    the_app = init_celery_app(amqp_conf)

    from apiumworker.contact import celery_config

    the_app.config_from_object(celery_config)

    return the_app, thrift_client


app, client = _init()

