#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/30 19:15'

from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class HtmlParser(object):

    def parse(self,response):
        html = response.content
        soup = BeautifulSoup(html, "lxml", from_encoding='utf-8')
        # 单个页面数据收集,new_urls,title,summary
        links = soup.find_all('a', href=re.compile(r'^/item/\S+'))
        new_urls = []
        for link in links:
            new_urls.append(urljoin(response.url, link['href']))
        titleNode = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')
        if titleNode:
            titleNode = titleNode.find('h1')  #加层判断来保护
        summaryNode = soup.find('div', class_='lemma-summary')
        if titleNode and summaryNode:
            title = titleNode.get_text()
            summary = summaryNode.get_text()
        else:
            return new_urls, None  # 做一下保护，可能没有简介。
        json_data = {'title': title, 'summary': summary}
        return new_urls, json_data

