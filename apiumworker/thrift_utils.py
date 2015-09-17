# coding=utf-8
__author__ = 'zephyre'

# Thrift调用相关函数


def init_client(host, port, service, **kwargs):
    """
    创建Thrift client
    :param host: 主机地址
    :param port: 端口
    :param service: Thrift服务
    :return: Thrift client对象
    """
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol

    socket = TSocket.TSocket(host, port)
    tranport = TTransport.TFramedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(tranport)
    tranport.open()

    return service.Client(protocol)