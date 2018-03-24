#-*- coding: utf-8 -*-

# author: li yangjin
from scrapy import cmdline

name = 'baike'
cmd = 'scrapy crawl %s' % name
print (cmd.split())
cmdline.execute(cmd.split())