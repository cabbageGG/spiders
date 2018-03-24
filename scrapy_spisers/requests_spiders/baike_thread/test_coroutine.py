#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/2 8:37'

import time
import asyncio

#联想生产者消费者模式的协程，构造url添加和取出模式，下载和解析模式，解析和数据存储模式。解析和URL添加模式

#1、url添加取出模式
#情景：开始有一个url，传递给url处理函数，处理完成，返回新的url给main函数，继续循环。但是，url的处理是有阻塞的。

#同步方式
#主函数
def main():
    urls = set(['a','b','c'])
    while True:
        if urls:
            url = urls.pop()
            new_url = handle_url(url)
            urls.add(new_url)
#处理url的生成器
def handle_url(url):
    time.sleep(5)
    new_url = url + '1'
    return new_url

#协程方式。总结：简简单单的协程方式，还只是单线程操作，碰到io阻塞(比如网络请求，读写数据)，还是会阻塞。要使用异步，才能避免阻塞的耗时。
#只管发送url
def main_async(handle_url_async):
    urls = set(['a','b','c'])
    url = urls.pop()
    while True:
        if url:
            handle_url_async.send(url)
#接收并处理url
def handle_url_async():
    #不停接收并生产新的url
    new_url = ''
    while True:
        r = yield new_url
        time.sleep(5)
        new_url = r + '1'








