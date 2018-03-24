#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/30 19:14'

class UrlManager():
    def __init__(self):
        self.urls = set()
        self.crawed_urls = set()

    def add_new_url(self,new_url):
        if new_url not in self.crawed_urls:
            self.urls.add(new_url)

    def add_new_urls(self,new_urls):
        for new_url in new_urls:
            self.add_new_url(new_url)

    @property
    def has_new_url(self):
        if len(self.urls) > 0:
            return True
        else:
            return False

    def get_new_url(self):
        url = self.urls.pop()
        if url in self.crawed_urls:
            return None
        else:
            self.crawed_urls.add(url)
            return url
