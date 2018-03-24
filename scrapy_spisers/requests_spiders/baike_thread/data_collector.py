#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/30 19:16'

import json

class DataCollector(object):

    #注：这里可以自定义收集数据的类型，比如：还可以插入mysql。
    def collect_data(self, json_data):
        with open('baike.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(json_data, ensure_ascii=False) + '\n') #注意：这里写入，想要保存中文的话。1、open加上encoding='utf-8' 2、write加上ensure_ascii=False


