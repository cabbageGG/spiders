#-*- coding: utf-8 -*-

# author: li yangjin
import requests,json
from w3lib.html import remove_tags

url = 'http://comment.ali213.net/ali-comment-ajax-2-3g.php?callback=success_jsonpCallbackcontent&action=display&appid=6&conid=26397&steamid=304530&page=1&_=1514454399511'
r = requests.get(url=url)
# print (r.text)
a = r.content.decode('unicode_escape')
a = remove_tags(a)
a = a[32:-2]
a = a.replace('\n','')
a = a.replace('\t','')
# a = a.replace(' ','')
print (a)
b = json.loads(a)
print (type(b))
print (b)


