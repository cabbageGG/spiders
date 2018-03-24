#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/31 20:10'

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import time

#联想生产者消费者模式的协程，构造url添加和取出模式，下载和解析模式，解析和数据存储模式。解析和URL添加模式
#1、url产生和提取模式。
def parse_url():
    new_urls = ''
    json_data = ''
    while True:
        url = yield new_urls,json_data
        response = download(url)    #这个下载的网络请求会造成阻塞，但是需要异步来避免这种耗时
        new_urls,json_data = parse(response)

def start(c,start_url,tasks):#接收一个函数
    urls = set()
    crawed_urls = set()
    c.send(None)
    url = start_url
    new_urls = ''
    json_data = ''
    count = 0
    while True:
        if url:
            new_urls,json_data = c.send(url)
        add_new_urls(new_urls,urls,crawed_urls)
        if json_data:
            collect_data(json_data)
            count = count + 1
        url = get_url(urls,crawed_urls)
        if count > tasks:
            break

def add_new_urls(new_urls,urls,crawed_urls):
    for new_url in new_urls:
        if new_url not in crawed_urls:
            urls.add(new_url)

def get_url(urls,crawed_urls):
    if len(urls) > 0:
        url = urls.pop()
    if url not in crawed_urls:
        crawed_urls.add(url)
        return url
    else:
        return None

def download(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    return response

def parse(response):
    soup = BeautifulSoup(response.content, "lxml", from_encoding='utf-8')
    # 单个页面数据收集,new_urls,title,summary
    links = soup.find_all('a', href=re.compile(r'^/item/\S+'))
    new_urls = []
    for link in links:
        new_urls.append(urljoin(start_url, link['href']))
    titleNode = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')
    if titleNode:
        titleNode = titleNode.find('h1')  # 加层判断来保护
    summaryNode = soup.find('div', class_='lemma-summary')
    if titleNode and summaryNode:
        title = titleNode.get_text()
        summary = summaryNode.get_text()
    else:
        return new_urls, None  # 做一下保护，可能没有。什么情况会没有？？
    json_data = {'title': title, 'summary': summary}
    return new_urls, json_data

def collect_data(json_data):
    print (json_data)
    with open('baike1.json','a',encoding='utf-8') as f:
        f.write(json.dumps(json_data,ensure_ascii=False)+'\n')

if __name__ == "__main__":
    start_url = 'https://baike.baidu.com/item/Python/407313'
    tasks = 5 #设置需要爬取的页面数
    c = parse_url()
    start_time = time.time()
    start(c,start_url,tasks)
    end_time = time.time()
    cost_time = end_time - start_time
    print("总共耗时：%s秒" % cost_time)

    # Thead7成功抓取第1000个页面
    # 结束
    # 总共耗时：99.16799998283386秒
