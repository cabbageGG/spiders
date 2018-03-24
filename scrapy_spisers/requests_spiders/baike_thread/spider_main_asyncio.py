#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/2 11:10'

import time
import html_parser,html_downloader, data_collector
from multiprocessing import Process,Queue,Value
import os

class spider_main(object):
    def __init__(self,start_url,tasks,concurrency_nums):
        self.count = Value('i',0)   #全局爬取页面计数
        self.q1 = Queue()
        self.q2 = Queue()
        self.start_url = start_url
        self.tasks = tasks
        self.concurrency_nums = concurrency_nums

    def start(self):
        #启动服务进程
        s = Process(target=server, args=(self.q1,self.q2,self.start_url))
        s.start()
        #开始工作进程
        print('开始爬取')
        processor_list = []
        for i in range(self.concurrency_nums):
            processor_name = 'Processor%s' % i
            p = Process(target=client,args=(self.q1,self.q2,self.tasks,self.count,self.concurrency_nums))
            processor_list.append(p)
        for p in processor_list:
            p.start()
        for p in processor_list:
            p.join()
        s.terminate()
        print('结束')

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


# TypeError: can't pickle weakref objects

# manager.dict里的字段不能用set。因为，这个不支持dict.add这种链式函数操作。只能简单的赋值操作。

# 新思路：制作一个服务进程，专门用于共享数据给所有子进程。
    # 基本流程是：需要两个队列，一个队列是待爬取的url，由服务进程产生，由各个子进程来消费取走；
    #             另一个队列是新产生的url，由子进程产生，然后由服务进程来消费取走，同时服务进程辨别是否需要加入到第一个队列中。
    #
    # 从上面的分析，我们需要两个队列来实现进程间的数据共享。
    # 同时，需要把url管理器的逻辑写入一个服务进程中，而调度器的逻辑写入到子进程中。

    # q1 = Queue()
    # q2 = Queue()
    # q1 服务进程产生,子进程消费；q2 子进程产生，服务进程消费
    # count = Value('i',0) 子进程共享已爬取的数目，作为子进程是否结束的标志。

    def server(q1,q2):
        crawed_urls = set()
        q1.put(start_url)
        while True:
            new_url = q2.get()
            if new_url not in crawed_urls:
                q1.put(new_url)
                crawed_urls.add(new_url)

    def client(q1,q2,tasks,count):
        while True:
            url = q1.get()
            new_urls, data = craw(url,tasks,count)
            for new_url in new_urls:
                q2.put(new_url)

    def craw(url,tasks,count):
        pass

    #补充：像q1.put q1.get 等操作是会有阻塞的。他们也是默认阻塞的。这时，就可以使用协程来避免这种阻塞。(好像这种阻塞可以忽略)
    #思路：将这个逻辑------q1 服务进程产生,子进程消费；q2 子进程产生，服务进程消费
    #      改写为----------q1 main函数产生,子函数消费；q2 子函数产生，main函数消费
    #暂时不考虑进程，先实现q1
    def producer1(c,q2):
        crawed_urls = set()
        while True:
            if q2:
                url = q2.pop()
                c.send(url)

    def consumer1(q1):
        url = ''
        new_url = ''
        while True:
            url = yield new_url
            q1.add(url)

    def c():
        value = ''
        while True:
            r = yield value
            #消费过程
            value = r + '1'

    def p(c):
        c.send(None)
        for i in range(5):
            a = c.send(str(i))
            print ("消费返回结果：%s" % a)

    #定义全局变量
    urls = set()
    craw_urls = set()
    def send_url(c):
        c.send(None)
        while True:
            if urls:
                url = urls.pop()
                r = c.send(url)
                print("消费返回结果：%s" % r)
    def parse_url():
        value = ""
        while True:
            r = yield value
            if not r:
                return
            # 消费过程
            #todo
            # 消费结果
            value = "200 OK"











