#-*- coding: utf-8 -*-

# author: li yangjin

import requests
import json
import re
import time
from random import randint

ss = requests.session()

url = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0"

headers = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Content-Length":"25",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"user_trace_token=20171126160027-dd5dbcbc-d27f-11e7-9a6d-5254005c3644; LGUID=20171126160027-dd5dc2ad-d27f-11e7-9a6d-5254005c3644; index_location_city=%E5%B9%BF%E5%B7%9E; JSESSIONID=ABAAABAAADEAAFI6F486ACF95690012A8CBF0154DCE8516; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3Dsug%26fromSearch%3Dtrue%26suginput%3Dp; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; _gat=1; _ga=GA1.2.1397294834.1511683109; _gid=GA1.2.553114411.1514440517; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512626763,1514440517; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514450705; LGSID=20171228164232-0bb67ea1-ebab-11e7-9ebb-5254005c3644; LGRID=20171228164729-bc82b8a0-ebab-11e7-9ebb-5254005c3644; TG-TRACK-CODE=search_code",
    "Host":"www.lagou.com",
    "Origin":"https://www.lagou.com",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "X-Anit-Forge-Code":"0",
    "X-Anit-Forge-Token":"None",
    "X-Requested-With":"XMLHttpRequest"
}

ss.headers=headers

data = {
    'first':'true',
    'pn':'1',
    'kd':'python'
}

# r = ss.post(url=url, data=data)
# print(r.status_code)
# print(r.text)

import MySQLdb
conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="scrapy",port=3306,charset="utf8",use_unicode=True)
cursor = conn.cursor()
sql = """
      insert into lagou_python1 (companyName,companySize,createTime,positionLable,positionName,salary_min,salary_max,workYear,city)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
     """

for i in range(1,95):
    if i is 1:
        data['first'] = 'true'
    else:
        data['first'] = 'false'
    data['pn'] = str(i)
    r = ss.post(url=url, data=data)
    print (r.status_code)
    print (r.text)
    ret_json = json.loads(r.text)
    results = ret_json["content"]["positionResult"]["result"]
    for result in results:
        companyName = result["companyFullName"]
        companySize = result["companySize"]
        createTime = result["createTime"]
        positionLables = ",".join(result["positionLables"])
        positionName = result["positionName"]
        salary = result["salary"]
        match = re.match(r'(\d+)k-(\d+)k', salary)
        if match:
            salary_min = int(match.group(1))
            salary_max = int(match.group(2))
        else:
            salary_min = 0
            salary_max = 0
        workYear = result["workYear"]
        city = result["city"]
        params = (companyName, companySize, createTime, positionLables, positionName, salary_min, salary_max, workYear,city)
        cursor.execute(sql, params)
        conn.commit()
    s = randint(10,20)
    time.sleep(s)

cursor.close()
conn.close()