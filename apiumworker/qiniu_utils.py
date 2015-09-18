# coding=utf-8
from apiumworker import get_config

__author__ = 'zephyre'


# 七牛相关的函数


qiniu_ak = str(get_config(conf_names=['apiumworker'], cache_key='apiumworker-conf')['apiumworker']['qiniu']['accessKey'])
qiniu_sk = str(get_config(conf_names=['apiumworker'], cache_key='apiumworker-conf')['apiumworker']['qiniu']['secretKey'])


def get_qiniu_url(bucket, key, style, private=False, expires=7 * 24 * 3600):
    """
    默认情况下，图像资源都是host在七牛上的。给定bucket和key，通过本函数，可以返回图像在七牛上的url
    :param bucket: 图像资源bucket对应的域名
    :param key:
    :param style: 图像的处理样式。现在支持thumb和full两种，分别返回缩略图和大图。如果为None，则不启用图像处理流程，直接返回原图。
    :param private: 是否为私有资源。如果为True，将尝试计算token并返回私有地址。
    :param expires: 设置url过期时间。默认为7天。如果private为False（公有资源），该选项不起作用。
    :return:
    """
    from qiniu import Auth

    qiniu_client = Auth(qiniu_ak, qiniu_sk)
    base_url = 'http://%s/%s' % (bucket, key)
    style_url = '%s!%s' % (base_url, style) if style else base_url

    if private:
        return qiniu_client.private_download_url(style_url, expires=expires)
    else:
        return style_url
