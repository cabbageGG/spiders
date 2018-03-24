# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
import re
from datetime import datetime

def replaceTag(value):
    return value.replace('·','').strip()

def getNum(value):
    m = re.match(r'.*?(\d+).*',value)
    if m:
        return int(m.group(1))
    else:
        return 0

def remove_comment(value):
    if "评论" in value:
        return ''
    else:
        return value

class ScrapySpisersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class JobboleItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(replaceTag),
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment),
        output_processor=Join(','),
    )
    vote_nums = scrapy.Field(
        input_processor=MapCompose(getNum),
    )
    mark_nums = scrapy.Field(
        input_processor=MapCompose(getNum),
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(getNum),
    )
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags),
    )
    front_img_url = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field() #定义为item的唯一识别码

    def get_sql_params(self):
        sql = """
             insert into jobbole (url_id,url,title,tags,create_time,craw_time,vote_nums,content) 
             values (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE vote_nums=VALUES(vote_nums)
             """
        craw_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        params = (self["url_id"], self["url"], self["title"], self["tags"], self["create_time"],
                  craw_time, self["vote_nums"], self["content"])
        return sql,params

class zhihu_question_item(scrapy.Item):
    question_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    keywords = scrapy.Field()
    answerCount = scrapy.Field()
    commentCount = scrapy.Field()
    dateCreated = scrapy.Field()
    dateModified = scrapy.Field()
    visitsCount = scrapy.Field()
    followerCount = scrapy.Field()
    content = scrapy.Field()

    def get_sql_params(self):
        sql = """
             insert into zhihu_question (question_id,title,url,url_id,keywords,answerCount,
             commentCount,dateCreated,dateModified,visitsCount,followerCount,content,craw_time) 
             values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE dateModified=VALUES(dateModified)
             """
        craw_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        params = (self["question_id"], self["title"], self["url"], self["url_id"], self["keywords"],self["answerCount"],
                  self["commentCount"],self["dateCreated"],self["dateModified"],self["visitsCount"],self["followerCount"],
                  self["content"],craw_time)
        return sql,params

class zhihu_answer_item(scrapy.Item):
    answer_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()

    def get_sql_params(self):
        sql = """
             insert into zhihu_answer (answer_id,url,question_id,author_id,content,praise_num,
             comments_num,create_time,update_time,craw_time) 
             values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE update_time=VALUES(update_time),content=VALUES(content)
             """
        create_time = datetime.fromtimestamp(self["create_time"]).strftime("%Y/%m/%d %H:%M:%S")
        update_time = datetime.fromtimestamp(self["update_time"]).strftime("%Y/%m/%d %H:%M:%S")
        craw_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        params = (self["answer_id"], self["url"], self["question_id"], self["author_id"], self["content"],self["praise_num"],
                  self["comments_num"],create_time,update_time,craw_time)
        return sql,params


class baikeItem(scrapy.Item):
    title = scrapy.Field()
    summary = scrapy.Field()
