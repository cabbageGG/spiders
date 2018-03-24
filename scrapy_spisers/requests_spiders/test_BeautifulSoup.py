#-*- coding: utf-8 -*-

# author: li yangjin
from bs4 import BeautifulSoup
import re

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

#html.parser 测试
#find_all( name=None , attrs:{} , recursive=True , string , **kwargs )
soup = BeautifulSoup(html,'html.parser')
links1 = soup.find_all('a')
print ("links1:",links1)
links2 = soup.find_all('a',{"id":"link2"},recursive=True)
print ("links2:",links2)
links3 = soup.find_all('a',href=re.compile(r'ill'))
print ("links3:",links3)

links4 = soup.select('#link3') #可直接传入css选择器语句
print ("links4:",links4)

#lxml 测试
soup = BeautifulSoup(html,'lxml')
links1 = soup.find_all('a')
print ("links1:",links1)
links2 = soup.find_all('a',{"id":"link2"},recursive=True)
print ("links2:",links2)
links3 = soup.find_all('a',href=re.compile(r'ill'))
print ("links3:",links3)

links4 = soup.select('#link3') #可直接传入css选择器语句
print ("links4:",links4)

body = soup.find('body')
text1 = body.get_text()
text2 = body.text
text3 = body.string #None
text4 = links4[0].string #Tillie
print('text1',text1)
print('text2',text2)
print('text3',text3)
print('text4',text4)

