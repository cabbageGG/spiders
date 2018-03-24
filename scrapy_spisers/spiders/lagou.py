# -*- coding: utf-8 -*-
import scrapy


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=']

    def parse(self, response):
        pass
