#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/2 13:47'

import requests
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import asyncio
import aiohttp

def get_urls(num):
    start_url = 'https://baike.baidu.com/item/Python/407313'
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    s = requests.session()
    s.headers=headers
    #页面下载
    r = s.get(url=start_url)
    soup = BeautifulSoup(r.content,"lxml",from_encoding='utf-8')   #注意：这里使用r.content ，而不是r.text。否则，就会忽略from_encoding。
    #页面url提取
    links = soup.find_all('a',href=re.compile(r'^/item/\S+'))
    urls = set()
    for i in range(num):
        urls.add(urljoin(start_url,links[i]['href']))
    return urls

def request_url(url):
    requests.get(url=url,headers=headers)

@asyncio.coroutine
def aiohttp_request_url(url):
    response = yield from aiohttp.ClientSession().get(url=url,headers=headers)
    # response = yield from aiohttp.request(method='GET',url=url,headers=headers)
    content = yield from response.read()
    return content

@asyncio.coroutine
def get_res(url):
    res = yield from aiohttp_request_url(url)
    print(res)
    return url

def start_test(urls):
    tasks = [get_res(url) for url in urls]
    loop = asyncio.get_event_loop()
    res,_ = loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    print(len(res),res)



if __name__ == "__main__":
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    urls = get_urls(10)
    start_time = time.time()
    # for url in urls:
    #     print (url)
    #     request_url(url)
    start_test(urls)
    end_time = time.time()
    cost_time = end_time - start_time
    print("总共耗时：%s秒" % cost_time)

    # 总共耗时：4.317999839782715秒
    # 总共耗时：1.2200000286102295秒

    # Unclosed client session
    # client_session: <aiohttp.client.ClientSession object at 0x0000000003E138D0>