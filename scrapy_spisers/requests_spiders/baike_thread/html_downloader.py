#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/30 19:16'

import requests

class HtmlDownloader(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        }
        #注：初始化这里还可以加入session，cookies，proxy等

    def download(self,url):
        return requests.get(url=url,headers=self.headers)


