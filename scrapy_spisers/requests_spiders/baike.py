#-*- coding: utf-8 -*-

# author: li yangjin

import requests
from bs4 import BeautifulSoup
import re
# from urllib.parse import urljoin
import json
import time
from urllib.request import urlretrieve


# start_url = 'https://baike.baidu.com/item/Python/407313'
# headers = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
# }
# s = requests.session()
# s.headers=headers
# #页面下载
# r = s.get(url=start_url)
# #目标分析
# #提取页面的全部链接,然后爬取链接，获取title和简介内容，同时返回该链接页面的所有新的链接。
# #链接:<a href='/item/xxxxx'>
# #title:<dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1></dd>
# #简介:<div class="lemma-summary" label-module="lemmaSummary"><div class="para" label-module="para">Python</div></div>
# soup = BeautifulSoup(r.content,"lxml",from_encoding='utf-8')   #注意：这里使用r.content ，而不是r.text。否则，就会忽略from_encoding。
# #页面url提取
# links = soup.find_all('a',href=re.compile(r'^/item/\S+'))
# urls = set()
# crawed_urls = set()
# for i in range(5):
#     print (links[i]['href'])
#     urls.add(urljoin(start_url,links[i]['href']))
#     urls.add(urljoin(start_url,links[i]['href']))
# #单个页面数据收集
# title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
# print(title.text)
# summary = soup.find('div',class_='lemma-summary')
# print(summary.text)

def download_html(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    html = requests.get(url=url,headers=headers).content
    return html

def parse_html(html):
    soup = BeautifulSoup(html, "lxml", from_encoding='utf-8')
    # 单个页面数据收集,new_urls,title,summary
    links = soup.find_all('a', href=re.compile(r'^/item/\S+'))
    new_urls = []
    for link in links:
        new_urls.append(urljoin(start_url, link['href']))
    titleNode = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
    summaryNode = soup.find('div', class_='lemma-summary')
    if titleNode and summaryNode:
        title = titleNode.get_text()
        summary = summaryNode.get_text()
    else:
        return new_urls,None                 #做一下保护，可能没有。什么情况会没有？？
    json_data = {'title':title,'summary':summary}
    return new_urls,json_data

def get_url(urls,crawed_urls):
    url = urls.pop()
    if url in crawed_urls:
        return None
    else:
        crawed_urls.add(url)
        return url

def add_new_urls(new_urls, urls,crawed_urls):
    for new_url in new_urls:
        if new_url not in crawed_urls:
            urls.add(new_url)

def collect_data(json_data):
    print (json_data)
    with open('baike.json','a',encoding='utf-8') as f:
        f.write(json.dumps(json_data,ensure_ascii=False)+'\n')   #注意：这里写入，想要保存中文的话。1、open加上encoding='utf-8' 2、write加上ensure_ascii=False

def spider_start(start_url, tasks):
    urls = set()
    urls.add(start_url)
    crawed_urls = set()
    count = 0  # 成功爬取的页面计数.
    print('开始爬取')
    while True:
        # 循环提取下一个url页面
        if urls:
            url = get_url(urls,crawed_urls)
            if url:
                response = download_html(url)
                new_urls, json_data = parse_html(response)
                add_new_urls(new_urls,urls,crawed_urls)
                if json_data:
                    collect_data(json_data)
                else:
                    print('fail url: %s' % url) #打印失败的url
                    continue
                count = count + 1
                print('成功抓取第%s个页面' % count)
        if count >= tasks:
            break
    print('结束')

if __name__ == "__main__":
    start_url = 'https://baike.baidu.com/item/Python/407313'
    tasks = 5 #设置需要爬取的页面数
    start_time = time.time()
    spider_start(start_url,tasks)
    end_time = time.time()
    cost_time = end_time - start_time
    print("总共耗时：%s秒" % cost_time)

    # 成功抓取第1000个页面
    # 结束
    # 总共耗时：589.6420001983643秒







