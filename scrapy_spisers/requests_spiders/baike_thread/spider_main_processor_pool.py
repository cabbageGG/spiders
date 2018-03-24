#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/31 17:59'

import time
import html_parser,html_downloader, data_collector
from multiprocessing import Process,Queue,Value,Pool,Manager
import os

class spider_main(object):
    def __init__(self,start_url,tasks,concurrency_nums):
        self.count = Manager().Value('i',0)   #全局爬取页面计数
        self.q1 = Manager().Queue()
        self.q2 = Manager().Queue()
        self.start_url = start_url
        self.tasks = tasks
        self.concurrency_nums = concurrency_nums

    def start(self):
        #启动服务进程
        s = Process(target=server, args=(self.q1,self.q2,self.start_url))
        s.start()
        #开始工作进程
        print('开始爬取')
        p = Pool(self.concurrency_nums)  # 设置进程池大小，可以同时运行的进程数量
        for i in range(self.concurrency_nums):  # 创建进程
            p.apply_async(client, args=(self.q1,self.q2,self.tasks,self.count,self.concurrency_nums))
        print('Waiting for all subprocesses done...')
        p.close()  # 关闭进程池
        p.join()  # 等待进程全部执行完
        s.terminate()
        print('结束')

def test(*args):
    print("启动工作进程%s" % os.getpid())
    time.sleep(5)

def server(q1,q2,start_url):
    print("启动服务进程%s" % os.getpid())
    crawed_urls = set()
    q1.put(start_url)
    while True:
        new_url = q2.get()
        if new_url not in crawed_urls:
            q1.put(new_url)
            crawed_urls.add(new_url)

def client(q1,q2,tasks,count,processor_nums):
    print("启动工作进程%s" % os.getpid())
    #初始化
    parser = html_parser.HtmlParser()
    downloader = html_downloader.HtmlDownloader()
    collector = data_collector.DataCollector()
    crawed_nums = 0

    while True:
        url = q1.get()
        response = downloader.download(url)
        new_urls, json_data = parser.parse(response)
        for new_url in new_urls:
            q2.put(new_url)
        if json_data:
            collector.collect_data(json_data)
            count.value = count.value + 1
            print('进程%s成功抓取第%s个页面' % (os.getpid(), count.value))
            crawed_nums = crawed_nums + 1
        else:
            print('fail url: %s' % url)  # 打印失败的url
        if count.value >= (tasks-processor_nums+1):
            print("%s爬取的网页数量：%s" % (os.getpid(), crawed_nums))
            break

if __name__ == "__main__":
    start_url = 'https://baike.baidu.com/item/Python/407313'
    tasks = 1000 #设置需要爬取的页面数
    concurrency_nums = 10 #设置并发数
    spider = spider_main(start_url,tasks, concurrency_nums)
    start_time = time.time()
    spider.start()
    end_time = time.time()
    cost_time = end_time - start_time
    print("总共耗时：%s秒" % cost_time)

    # 10个工作进程并发
    # 进程4796成功抓取第1000个页面
    # 结束
    # 总共耗时：60.52300000190735秒

    # 4个工作进程并发
    # 进程6088成功抓取第1000个页面
    # 结束
    # 总共耗时：133.8259997367859秒



