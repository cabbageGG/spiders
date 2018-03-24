# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs,json
from scrapy.exporters import JsonItemExporter
import MySQLdb,MySQLdb.cursors
from datetime import datetime
from twisted.enterprise import adbapi
import time

class ScrapySpisersPipeline(object):
    def process_item(self, item, spider):
        a = item
        print (a)
        print (type(a))
        return item

class JsonFilePipeline(object):
    def __init__(self):
        self.file = codecs.open("baike.json","w",encoding="utf-8")
        self.count = 0
        self.start_time = time.time()

    def process_item(self,item,spider):
        #序列化为json字符串
        data = json.dumps(dict(item),ensure_ascii=False) + "\n"  #注意这里需要手动换行 #注意需要加上ensure_ascii=False，否则中文显示不正常
        self.file.write(data)
        self.count = self.count + 1
        if self.count >= 1000:
            print("-------------------------------")
            print("总共耗时：%s秒" % (time.time()-self.start_time))
        else:
            return item

    def close_spider(self,spider):
        print("close")
        self.file.close()

class JsonExportPipeline(object):
    def __init__(self):
        self.file = open("jobboleExport.json","wb")
        self.exporter = JsonItemExporter(self.file, encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        self.exporter.export_item(item)  #用一个list来存储所有的dict。
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

class MySQLPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="scrapy",port=3306,charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        sql, params = item.get_sql_params()
        self.cursor.execute(sql,params)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

class MySQLTwistedPipeline(object):
    # scrapy 异步mysql导入
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error,item,spider) #处理异常

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        sql, params = item.get_sql_params()
        cursor.execute(sql, params)

    def handle_error(self,failure, item, spider):
        # 处理异步插入的异常
        print(failure)



