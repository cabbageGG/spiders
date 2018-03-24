#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/30 18:59'

import time
import url_manager, html_parser,html_downloader, data_collector
import threading

class spider_main(object):
    def __init__(self):
        self.urlManager = url_manager.UrlManager()
        self.parser = html_parser.HtmlParser()
        self.downloader = html_downloader.HtmlDownloader()
        self.collector = data_collector.DataCollector()
        self.lock = threading.Lock()    #线程锁
        self.local_crawed = threading.local() #创建全局ThreadLoacl对象,让每个线程拥有自己的数据。
        self.count = 0   #全局爬取页面计数

    def start(self, start_url, tasks, thread_nums):
        thread_list = []
        for i in range(thread_nums):
            thread_name = 'Thead%s' % i
            t = threading.Thread(target=self.thread,args=(tasks,thread_nums,),name=thread_name)
            thread_list.append(t)
        self.urlManager.add_new_url(start_url)
        print('开始爬取')
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        print('结束')

    def thread(self,tasks,thread_nums):
        self.local_crawed.nums = 0
        while True:
            # 先获取锁
            self.lock.acquire()
            try:
                if self.urlManager.has_new_url:
                    url = self.urlManager.get_new_url()
                else:
                    url = ''
            finally:
                self.lock.release()
            if url:
                response = self.downloader.download(url)
                new_urls, json_data = self.parser.parse(response)
                # 先获取锁
                self.lock.acquire()
                try:
                    self.urlManager.add_new_urls(new_urls)
                    if json_data:
                        self.collector.collect_data(json_data)
                        self.count = self.count + 1
                        print('%s成功抓取第%s个页面' % (threading.current_thread().name, self.count))
                        self.local_crawed.nums = self.local_crawed.nums + 1
                    else:
                        print('fail url: %s' % url)  # 打印失败的url
                finally:
                    self.lock.release()
            if self.count >= (tasks-thread_nums+1):
                print ("%s爬取的网页数量：%s" % (threading.current_thread().name,self.local_crawed.nums))
                break

if __name__ == "__main__":
    start_url = 'https://baike.baidu.com/item/Python/407313'
    tasks = 100 #设置需要爬取的页面数
    thread_nums = 4 #设置并发数
    spider = spider_main()
    start_time = time.time()
    spider.start(start_url,tasks, thread_nums)
    end_time = time.time()
    cost_time = end_time - start_time
    print("总共耗时：%s秒" % cost_time)

    # Thead7成功抓取第1000个页面
    # 结束
    # 总共耗时：99.16799998283386秒