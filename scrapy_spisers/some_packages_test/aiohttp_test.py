#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/15 15:43'

'''
官方文档：http://aiohttp.readthedocs.io/en/stable/client_reference.html
'''

from time import strftime,time
import aiohttp
import asyncio

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

session = aiohttp.ClientSession()
session._default_headers = headers

async def request_url(url):
    # async with aiohttp.ClientSession() as session:   #使用session,解决Session没有关闭报错问题
    async with session.get(url=url) as r:
        assert r.status == 200
        return await r.read()


async def get_c(url):
    c = await request_url(url)
    print(c)
    return url

def start_with_aiohttp(urls):
    tasks = [get_c(url) for url in urls]
    loop = asyncio.get_event_loop()
    res,_ = loop.run_until_complete(asyncio.wait(tasks))
    print(session)
    session.close()
    loop.close()
    print(len(res),res)

if __name__ == "__main__":
    urls = ['https://www.baidu.com','https://www.baidu.com','https://www.baidu.com']
    s_time = time()
    start_with_aiohttp(urls)
    print("cost:%.2f秒" % (time()-s_time))