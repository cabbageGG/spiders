#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/2 22:17'

from urllib.request import urlretrieve
import requests

url = 'http://www.xiaohuar.com/d/file/20170917/715515e7fe1f1cb9fd388bbbb00467c2.jpg'

# urlretrieve(url, '1.jpg')

r = requests.get(url)

with open('2.jpg','wb') as f:
    f.write(r.content)


