#-*- coding: utf-8 -*-

# author: li yangjin

import requests
from scrapy.selector import Selector
from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path="C:/opt/chromedriver.exe")

browser.get("http://www.zhihu.com/")

browser.find_element_by_css_selector("div.SignFlow-accountInput.Input-wrapper input.Input").send_keys("13246856469")
browser.find_element_by_css_selector("div.SignFlow-password div.SignFlowInput div.Input-wrapper input.Input").send_keys("")
browser.find_element_by_css_selector("button.SignFlow-submitButton").click()
print (browser.get_cookies())
print (browser.get)
for i in range(10):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    time.sleep(3)
t_slelector = Selector(text=browser.page_source)

"""
accept:application/json, text/plain, */*
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9
authorization:oauth c3cef7c66a1843f8b3a9e6a1e3160e20
Connection:keep-alive
Cookie:_zap=fb291a5e-10a4-4bec-a7cb-8edcc03c6e16; d_c0="AABCBeUNlQyPTo8xECg3e4T3nC4XSf88Bm4=|1508941293"; aliyungf_tc=AQAAAFt0y0JgCAAAVK1gcJGmZDRd4z0l; q_c1=9e716ce9fb4c4585a10efe6b9748dc23|1514339839000|1508934038000; l_cap_id="MmQ3ZjM2YThkZWFjNGIxNWJiYzIzMjEwYjVjZmI4Nzg=|1514341101|822ccb2eb4b5fea703cdb47a34601371e2597266"; r_cap_id="MWU3MGI5ZGEwMWJiNDc5YzkxNGE0Y2E3OTBkYmMwYzA=|1514341101|85a275efc74c6ee8ff6c8bc63319bf66ac351b85"; cap_id="YTc2MTJkY2ZhM2RkNDgyNWE1NjVhOGIwZWU0N2NiNmQ=|1514341101|93a5b786442327291bcfd4b3a700e6abd539c038"; __utma=155987696.1256875915.1514268584.1514268584.1514356424.2; __utmc=155987696; __utmz=155987696.1514268584.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); capsion_ticket="2|1:0|10:1514360560|14:capsion_ticket|44:NGM4N2Q5ZTFiY2VjNDg1NmE5NDVlZDU3ZTk1NTc3YjM=|4e5ad55b4f970a6fcf1b94aca2c63c2d2bf84c3af11ddf5318c0c3fb4499c5b2"; _xsrf=ec2859e8-903e-467a-89c4-c5ac989d6f65
Host:www.zhihu.com
Referer:https://www.zhihu.com/question/30332628
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36
X-UDID:AABCBeUNlQyPTo8xECg3e4T3nC4XSf88Bm4=
"""

# url = 'https://www.zhihu.com/'
#
# s = requests.session()
#
# s.headers = {
#     "User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
#     "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
# }
#
# r = s.get(url=url)
#
# with open("test.html",'wb') as f:
#     f.write(r.content)

# print("headers")
# print(r.headers)
# print("cookies")
# print(r.cookies)
#
#url = 'http://www.zhihu.com/api/v4/questions/263421336/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=23'
# url = "https://www.zhihu.com/api/v4/questions/30332628/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default"
# for i in range(1):
#     r = s.get(url=url)
#     print (i)
#     print (r.status_code)
#     print (r.text)


