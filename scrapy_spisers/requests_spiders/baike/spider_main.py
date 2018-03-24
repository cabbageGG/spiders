#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/30 18:59'

import time
import url_manager, html_parser,html_downloader, data_collector

class spider_main(object):
    def __init__(self):
        self.urlManager = url_manager.UrlManager()
        self.parser = html_parser.HtmlParser()
        self.downloader = html_downloader.HtmlDownloader()
        self.collector = data_collector.DataCollector()

    def start(self, start_url, tasks):
        self.urlManager.add_new_url(start_url)
        count = 0
        print('开始爬取')
        while True:
            # 循环提取下一个url页面
            if self.urlManager.has_new_url:
                url = self.urlManager.get_new_url()
                if url:
                    response = self.downloader.download(url)
                    new_urls, json_data = self.parser.parse(response)
                    self.urlManager.add_new_urls(new_urls)
                    if json_data:
                        self.collector.collect_data(json_data)
                    else:
                        print('fail url: %s' % url)  # 打印失败的url
                        continue
                    count = count + 1
                    print('成功抓取第%s个页面' % count)
            if count >= tasks:
                break
        print('结束')

if __name__ == "__main__":
    start_url = 'https://baike.baidu.com/item/Python/407313'
    tasks = 1000 #设置需要爬取的页面数
    spider = spider_main()
    start_time = time.time()
    spider.start(start_url,tasks)
    end_time = time.time()
    cost_time = end_time - start_time
    print("总共耗时：%s秒" % cost_time)

    # 成功抓取第1000个页面
    # 结束
    # 总共耗时：766.4340000152588秒