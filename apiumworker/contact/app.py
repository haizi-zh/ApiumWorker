# coding=utf-8
__author__ = 'pengyt'


def __init_app():
    from celery import Celery
    from apiumworker.contact.users import userservice
    from thrift import Thrift
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol
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

    # conf = get_config(['contact', 'mongo'], ['contact', (apiumworker_name, 'apiumworker')], cache_key='contact')
    # conf_yunkai = conf['apiumworker']['mongo']
    # service_yunkai = conf['services']['mongo']

    # conf = get_config(['smscenter', 'rabbitmq'], ['smscenter', (apiumworker_name, 'apiumworker')], cache_key='sms')
    # conf_rabbitmq = conf['apiumworker']['rabbitmq']
    # service_rabbitmq = conf['services']['rabbitmq']
    conf = get_config(['yunkai', 'rabbitmq'], [(apiumworker_name, 'apiumworker')], cache_key='contact')
    # conf_name = conf['contact']['name']#contact
    # conf_port = conf['contact-dev']['port']#9000

    server_entries = conf['services']['yunkai'].values()
    # 默认只使用第一个节点
    host = server_entries[0]['host']
    port = server_entries[0]['port']

    conf_rabbitmq = conf['apiumworker']['rabbitmq']
    service_rabbitmq = conf['services']['rabbitmq']

    from apiumworker.contact import celery_config
    the_app = Celery('ApiumWorker', broker='amqp://%s:%s@%s:%d/%s' %
                                           (conf_rabbitmq['username'], conf_rabbitmq['password'],
                                            service_rabbitmq['host'], service_rabbitmq['port'],
                                            conf_rabbitmq['virtualhost']))
    the_app.config_from_object(celery_config)

    try:
        socket = TSocket.TSocket(host, port)
        tranport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(tranport)
        tranport.open()
        client = userservice.Client(protocol)

        return client, the_app
    except Thrift.TException, tx:
        print '%s' % (tx.message)
        raise

client, app = __init_app()

