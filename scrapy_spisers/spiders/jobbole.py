# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urljoin
from scrapy_spisers.items import JobboleItem,JobboleItemLoader
from scrapy.loader import ItemLoader
from scrapy_spisers.util.common import getMd5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['python.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        #提取url,根据页面特色，选择广度优先解析页面
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')

        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            img_url = post_node.css('img::attr(src)').extract_first("")
            yield Request(url=urljoin(response.url, post_url), callback=self.detail_parse, meta={"front_img_url":img_url})
        #下一页
        next_url = response.css('a.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield Request(url=urljoin(response.url, next_url), callback=self.parse)

    def detail_parse(self, response):

        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()
        # tags = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # vote_nums = response.xpath('//span[contains(@class,vote-post-up)]/h10/text()').extract()
        # mark_nums = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract()
        # comment_nums = response.xpath('//div[@class="post-adds"]/a/span[contains(@class, hide-on-480)]/text()').extract()

        # title = response.css('.entry-header h1::text').extract()
        # create_time = response.css('.entry-meta-hide-on-mobile ::text').extract_first()
        # tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tags = "-".join(tags)
        # vote_nums = response.css('.vote-post-up h10::text').extract()
        # mark_nums = response.css('.bookmark-btn ::text').extract()
        # comment_nums = response.css('.post-adds .hide-on-480 ::text').extract()
        # content = response.css('.entry').extract()
        front_img_url = response.meta.get("front_img_url", '')

        # jobboleItem = JobboleItem()  #这里实例化一个字典类型
        # jobboleItem["title"] = title
        # jobboleItem["create_time"] = create_time
        # jobboleItem["tags"] = tags
        # yield jobboleItem #字典类型数据返回，将item传入到pipeline的process_itme函数。

        # l = ItemLoader(item=JobboleItem(),response=response)  #使用默认ItemLoader
        l = JobboleItemLoader(item=JobboleItem(),response=response) #自定义JobboleItemLoader，继承自

        l.add_css("title",".entry-header h1::text")
        l.add_css("create_time",".entry-meta-hide-on-mobile ::text")
        l.add_css("tags",".entry-meta-hide-on-mobile a::text")
        l.add_css("vote_nums",".vote-post-up h10::text")
        l.add_css("mark_nums",".bookmark-btn ::text")
        l.add_css("comment_nums", ".post-adds .hide-on-480 ::text")
        l.add_css("content", ".entry")
        l.add_value("front_img_url", front_img_url)
        l.add_value("url", response.url)
        l.add_value("url_id", getMd5(response.url))

        jobboleItem = l.load_item()
        yield jobboleItem














