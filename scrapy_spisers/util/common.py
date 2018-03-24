#-*- coding: utf-8 -*-

# author: li yangjin
import hashlib
from fake_useragent import UserAgent

def getMd5(value):
    m = hashlib.md5()
    if isinstance(value,str):   #做一下判断，如果是unicode，则编码为utf-8。
        value = value.encode('utf-8')
    m.update(value)  #TypeError: Unicode-objects must be encoded before hashing
    return m.hexdigest()

def get_random_ip():
    return "http://127.0.0.1:80"

def get_zhihu_answer_url(question_id):
    return 'https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'.format(question_id)

def extendList(val, list=[]):
    list.append(val)
    return list


if __name__ == "__main__":
    # a = "12345中"
    # print(len(getMd5(a)))
    # ua = UserAgent()
    # print (ua.random)
    # print(get_zhihu_answer_url("1223"))
    list1 = extendList(10)
    list2 = extendList(123, [])
    list3 = extendList('a')

    print("list1 = %s" % list1)
    print("list2 = %s" % list2)
    print("list3 = %s" % list3)
