# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urljoin
from scrapy_spisers.items import baikeItem

class BaikeSpider(scrapy.Spider):
    name = 'baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/Python/407313']

    def parse(self, response):
        title = response.css('dd.lemmaWgt-lemmaTitle-title h1::text').extract_first("")
        summary = response.css('div.lemma-summary div::text').extract()
        summary = "".join(summary)
        item = baikeItem()
        item["title"] = title
        item["summary"] = summary
        yield item
        links = response.css('a[href^="/item/"]::attr(href)').extract()
        for link in links:
            yield Request(urljoin(response.url,link),callback=self.parse)

