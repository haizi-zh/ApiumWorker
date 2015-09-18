# coding=utf-8
__author__ = 'zephyre'


# 测试代码


if __name__ == '__main__':
    from apiumworker.qiniu_utils import *

    print qiniu_ak
    print qiniu_sk

    # 公开资源都放在下面这个bucket中
    bucket = 'images.taozilvxing.com'
    key = '000000276ec8f1cb64f3f930f4b0563f'
    print get_qiniu_url(bucket, key, None)

    # 尝试发送纯文本消息
    from apiumworker.hedy_utils import send_message, build_text_message

    msg = build_text_message(10001, 100056, u'我们来试试看吧')
    send_message(msg)
