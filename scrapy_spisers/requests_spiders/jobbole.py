#-*- coding: utf-8 -*-

# author: li yangjin
import requests

url = "http://python.jobbole.com/all-posts/"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

s = requests.get(url,headers=headers)

print(s.status_code)

print (s.content)

with open("jobbole.html","wb") as f:
    f.write(s.content)

