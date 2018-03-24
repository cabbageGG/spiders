#-*- coding: utf-8 -*-

# author: li yangjin

import requests,json,re
from w3lib.html import remove_tags

headers = {
    "accept":"application/json, text/plain, */*",
    "authorization":"Bearer 2|1:0|10:1514511561|4:z_c0|92:Mi4xelUzSEFnQUFBQUFBQUVJRjVRMlZEQ1lBQUFCZ0FsVk55T295V3dEb18zaFZ2S0FyaDBuS0RjWlBnQnVVVV9jbDhB|04b8ba9f4966aba9b694c4ac67843a9deac31c8ff3f2e4bcf01e5b81946e5b41",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Cookie":'_zap=fb291a5e-10a4-4bec-a7cb-8edcc03c6e16; d_c0="AABCBeUNlQyPTo8xECg3e4T3nC4XSf88Bm4=|1508941293"; q_c1=9e716ce9fb4c4585a10efe6b9748dc23|1514339839000|1508934038000; __utma=155987696.1256875915.1514268584.1514268584.1514356424.2; __utmz=155987696.1514268584.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAAHhmcmiFawYA9a1gcMqm3CBOSesd; l_cap_id="OGE3NWVmZjU1Yjg0NGZiMzg5NTM4NzJkNzBiNjRjMjU=|1514511545|c538960ffbf613dd1cb1964d1d9c06eed4916847"; r_cap_id="NzY5YzM0ZmY0ZTc3NGM1NmI2ZmQ2MDNlMTU0ZDZlYzU=|1514511545|7a289febb7570b835ad103306135e036deb02d5e"; cap_id="MDJjMDk3ODYzODZjNGEwN2FhMGViOGYxMDk0ZmUyN2M=|1514511545|02cc8c065bbffd9140f87dbafe6cba9fd22e5f09"; capsion_ticket="2|1:0|10:1514511546|14:capsion_ticket|44:YTgxODBhZjRmZjdkNDk2MGI3ZDFmMDU0NTU0MDA4MDk=|83ad9ad110bac500025e1f37c3a5c661b227649bf0312eb8b8c5d6d718d97f91"; z_c0="2|1:0|10:1514511561|4:z_c0|92:Mi4xelUzSEFnQUFBQUFBQUVJRjVRMlZEQ1lBQUFCZ0FsVk55T295V3dEb18zaFZ2S0FyaDBuS0RjWlBnQnVVVV9jbDhB|04b8ba9f4966aba9b694c4ac67843a9deac31c8ff3f2e4bcf01e5b81946e5b41"; _xsrf=6df49fb5-0dc2-4848-9eed-79cc44d6ed64',
    "Host":"www.zhihu.com",
    "Referer":"https://www.zhihu.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "X-API-VERSION":"3.0.53",
    "X-UDID":"AABCBeUNlQyPTo8xECg3e4T3nC4XSf88Bm4="
}

s = requests.session()

s.headers=headers

url = 'https://www.zhihu.com/api/v3/feed/topstory'

params = {
    "action_feed":"True",
    "limit":"10",
    "session_token":"1394bd7261e3f38d7ee91a6f051eab9e",
    "action":"down",
    "after_id":"9",
    "desktop":"true"
}
r = s.get(url=url, params=params)

print(r.status_code)
# a = r.content.decode('unicode_escape')
# # a = remove_tags(a)
# # a = a.replace('\n','')
# # a = a.replace('\t','')
# # print (a)
#
# #提取里面所有的文章或问题的url
# ret = re.findall(r'.*?(https://api.zhihu.com/(articles|questions)/.*?)"',a)
#
# if ret:
#     print(ret)
# else:
#     print('fail to get url')

b = r.json()
print(b)

# #替换json里不符合的双引号.
# #"brief": "{"source": "PR", "type": "feed_advert", "id": 10445}",
# ss = re.findall(r'("brief": "{"source": ".*?", "type": ".*?", "id": .*?}",)',a)
# print(ss)
#
# if ss:
#     for s in ss:
#         a = a.replace(s,'')
#
# # a = a.replace(' ','')
# print (a[4330:4440])
# print (a[4437])
# # b = json.loads(a)
# # print (type(b))
# # print (b)


