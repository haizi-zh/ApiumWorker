# coding=utf-8
import json
import requests

__author__ = 'zephyre'

from apiumworker.thrift_utils import init_client
from apiumworker.message.semat import SemaProcessor
from apiumworker.hedy_utils import *

semat_host = '192.168.100.2'
semat_port = 9588

semat_client = init_client(semat_host, semat_port, SemaProcessor)

# wenwen senderid
USERID_WENWEN = 10001

def process_text_message(kwargs):
    """
    处理发送给问问的纯文本消息
    :param text_message: 消息内容
    :return:
    """
    receiver = kwargs['senderId']
    # set basic tip, used for no result found
    tips = u'未找到，功能测试中....'
    # take out the message user send
    text = kwargs['contents']
    semantics = get_semantics(text)

    # based to scene to build different message
    # 'answer' is in semantics if it can match the intelligent Q&A
    if 'answer' in semantics:
        # 'answer' message is text
        qa_text = semantics['answer']['text']
        message = build_text_message(USERID_WENWEN, receiver,qa_text)
    # else case is the semantics, 'service' means the result is correct
    elif 'service' in semantics:
        service = semantics['service']
        semantic = semantics['semantic']
        if service == u'viewspots':
            proc_viewspots(semantic, receiver)
        elif service == u'restaurant':
            proc_restaurants(semantic, receiver)
        elif service == u'travelnotes':
            proc_travelnotes(semantic, receiver)
        else:
            pass
    # else case : only go to es for result
    # es need : set minimu_score, if too low , reurn one tip
    else:
        es_addr = '192.168.200.3:9210'
        es_index = 'accepted_qa'
        q_type = 'question'
        a_type = 'answer'

        q_data = json.dumps({"min_score": 2.2, "query": {"match": {"title": text}}})
        es_q_addr = 'http://%s/%s/%s/_search?size=100' % (es_addr, es_index, q_type)
        es_q_r = requests.get(es_q_addr, data=q_data)
        es_q_list = es_q_r.json()['hits']['hits']
        # if es_q_list is [], return 'test sentence'
        if not es_q_list:
            send_message(build_text_message(USERID_WENWEN, receiver, tips))
            return

        for qa_x in es_q_list:
            qid = qa_x['_source']['qid']
            q_title = qa_x['_source']['title']
            q_contents = qa_x['_source']['contents']

            es_a_addr = 'http://%s/%s/%s/_search?size=100' % (es_addr, es_index, a_type)
            a_data = json.dumps({"query": {"filtered": {"filter": {"term": {"qid": qid}}}}})
            es_a_r = requests.get(es_a_addr, data=a_data)
            es_a_list = es_a_r.json()['hits']['hits']
            if not es_a_list:
                send_message(build_text_message(USERID_WENWEN, receiver, tips))
                return

            a_contents = es_a_list[0]['_source']['contents']

            full_answer = u'问题题目：%s\n\n问题内容:%s\n\n问题答案:%s' % (q_title, q_contents, a_contents)
            # first test to return answer
            message = build_text_message(USERID_WENWEN, receiver, full_answer)
            send_message(message)
            return




def get_semantics(message):
    """
    调用讯飞接口，获得语义理解结果
    :param message:
    :return:
    """
    return json.loads(semat_client.understand(message))

api_dev_host = 'api-dev.lvxingpai.com'
api_host = 'api.lvxingpai.com'

def get_loc_id(city):
    # http://api-dev.lvxingpai.com/app/search?keyword=北京&loc=true
    api_addr = 'http://%s/app/search?keyword=%s&loc=true' % (api_dev_host, city)
    r = requests.get(api_addr)
    loc_id = r.json()['result']['locality']
    # nowdays, the loc_id is [] only results form the loc_id does not support country
    if loc_id :
        city_id = loc_id[0]['id']
    else:
        city_id = loc_id

    return city_id

def proc_viewspots(semantics, receiver):
    """
    处理关于景点的推荐问题
    :param semantics:
    :return:
    """
    vs_city = semantics['slots']['location']['city']
    vs_loc_id = get_loc_id(vs_city)
    # if vs_loc_id is null, it says should input city
    if not vs_loc_id:
        vs_tips = u'请输入城市名称^_^'
        send_message(build_text_message(USERID_WENWEN, receiver, vs_tips))
        return

    # http://api.lvxingpai.com/app/poi/viewspots?locality=5473ccd7b8ce043a64108c46&pageSize=5
    # 先取前5个结果，返回
    vs_num = 3
    vs_api = 'http://%s/app/poi/viewspots?locality=%s&pageSize=%d' % (api_host, vs_loc_id, vs_num)
    vs_r = requests.get(vs_api)
    vs_result_list = vs_r.json()['result']

    # vs_list = []
    # for x in vs_result_list:
    #     # zhName, enName
    #     vs_list.append(x['zhName'])
    # vs_str = ',\n'.join(vs_list)
    # vs_str_mark = u'给您推荐一些%s的景点：\n' % vs_city
    # return vs_str_mark + vs_str

    if not vs_result_list :
        # city is usually easy to be found
        vs_tips = u'请输入城市名称^_^'
        send_message(build_text_message(USERID_WENWEN, receiver, vs_tips))
        return

    # to this means it must have results about viewspots
    # output a bit tips before display relust
    vs_result_tips = u'下面这些%s的景点很不错哟' % vs_city
    send_message(build_text_message(USERID_WENWEN, receiver, vs_result_tips))
    for vs_x in vs_result_list:
        vs_id = vs_x['id']
        vs_image = vs_x['images']
        if vs_image:
            vs_image = vs_image[0]['url']
        vs_name = vs_x['zhName']

        send_message(build_viewspot_message(USERID_WENWEN, receiver, vs_id, vs_name, vs_image))
        # no appending 'break', the num of send messages depends on loop times


def proc_restaurants(semantics, receiver):
    """
    处理关于餐厅的推荐问题
    :param semantics:
    :return:
    """
    rs_city = semantics['slots']['location']['city']
    rs_loc_id = get_loc_id(rs_city)
    # if vs_loc_id is null, it says should input city
    if not rs_loc_id:
        rs_tips = u'请输入城市名称^_^'
        send_message(build_text_message(USERID_WENWEN, receiver,rs_tips))
        return

    # http://api.lvxingpai.com/app/poi/restaurants?locality=5473ccd7b8ce043a64108c46&pageSize=5
    # 先取前5个结果，返回
    rs_num = 3
    rs_api = 'http://%s/app/poi/restaurants?locality=%s&pageSize=%d' % (api_host, rs_loc_id, rs_num)
    rs_r = requests.get(rs_api)
    rs_result_list = rs_r.json()['result']
    # rs_list = []
    # for x in rs_result_list:
    #     # zhName, enName
    #     rs_list.append(x['zhName'])
    # rs_str = ',\n'.join(rs_list)
    #
    # rs_str_mark = u'给您推荐一些%s的美食：\n' % rs_city
    #
    # return rs_str_mark + rs_str

    if not rs_result_list:
        rs_tips = u'请输入城市名称^_^'
        send_message(build_text_message(USERID_WENWEN, receiver, rs_tips))
        return

    rs_result_tips = u'下面这些%s的美食很不错哟' % rs_city
    send_message(build_text_message(USERID_WENWEN, receiver, rs_result_tips))
    for rs_x in rs_result_list:
        rs_id = rs_x['id']
        rs_image = rs_x['images']
        if rs_image:
            rs_image = rs_image[0]['url']
        rs_name = rs_x['zhName']
        rs_style = rs_x['style']
        if rs_style:
            rs_style = rs_style[0]

        send_message(build_restaurant_message(USERID_WENWEN, receiver, rs_id, rs_name, rs_image, desc=rs_style))
        # no appending 'break', the num of send messages depends on loop times


def proc_travelnotes(semantics, receiver):
    """
    处理关于游记的推荐问题
    :param semantics:
    :return:
    """
    tn_city = semantics['slots']['location']['city']
    # http://api.lvxingpai.com/app/travelnotes?query=北京&pageSize=10
    # 先取前10个结果，返回
    tn_num = 10
    tn_api = 'http://%s/app/travelnotes?query=%s&pageSize=%d' % (api_host, tn_city, tn_num)
    tn_r = requests.get(tn_api)
    tn_result_list = tn_r.json()['result']
    # tn_list = []
    # for x in tn_result_list:
    #     # zhName, enName
    #     tn_list.append(x['summary'])
    # tn_str = u'\n----华丽的分割线----\n'.join(tn_list)
    # tn_str_mark = u'给您推荐一些%s游记摘要:\n' % tn_city
    # return tn_str_mark + tn_str

    if not tn_result_list:
        tn_tips = u'找不到关于%s的游记' % tn_city
        send_message(build_text_message(USERID_WENWEN, receiver, tn_tips))
        return

    # tn_result_tips = u''
    # send_message(build_text_message(USERID_WENWEN, receiver, tn_result_tips))
    for tn_x in tn_result_list:
        tn_id = tn_x['id']
        tn_images = tn_x['images']
        if tn_x['images']:
            tn_images = tn_images[0]['url']
        tn_name = tn_x['title']
        tn_url = tn_x['detailUrl']
        tn_summary = tn_x['summary']

        send_message(build_travelnote_message(USERID_WENWEN, receiver, tn_id, tn_url, tn_name, tn_images,
                                              desc=tn_summary))
        return
