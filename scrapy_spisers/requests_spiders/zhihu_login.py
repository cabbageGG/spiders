#-*- coding: utf-8 -*-

# author: li yangjin

import requests
import re
import json
import hmac
from hashlib import sha1
from time import time

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
}

s = requests.session()
s.headers = headers

client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
grant_type = 'password'
timestamp = str(int(time()*1000))
print (timestamp)
source = 'com.zhihu.web'
key = b'd1b964811afb40118a12068ff74a12f4'


def get_signature():
    h = hmac.new(key,digestmod=sha1)
    h.update(grant_type.encode('utf-8'))
    h.update(client_id.encode('utf-8'))
    h.update(source.encode('utf-8'))
    h.update(timestamp.encode('utf-8'))
    return h.hexdigest()

def login():
    signature = get_signature()
    login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
    # captcha:{"img_size":[200,44],"input_points":[[118.667,24.2708],[166.667,22.2708]]}
    # 大约连续输入错误密码5次，出现倒立文字校验码。
    input_points = get_capt()
    captcha = ""
    if not input_points:
        captcha = {"img_size":[200,44],"input_points":input_points}
        captcha = json.dumps(captcha)
    post_data = {
        "client_id":client_id,
        "grant_type":grant_type,
        "timestamp":timestamp,
        "source":source,
        "signature":signature,
        "username":"+8613246856469",
        "password":"",
        "captcha":captcha,
        "lang":"en",
        "ref_source":"homepage",
        "utm_source":""
    }
    r = s.post(login_url, data=post_data)

    print ("登录请求状态："+str(r.status_code))
    print(r.content)
    ret_json = json.loads(r.text, encoding='utf-8')
    msg = ret_json.get("msg","")
    print ("登录返回结果："+msg)


def get_capt():
    # capt_url = "https://www.zhihu.com/captcha.gif?type=login&lang=cn"
    capt_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=cn"
    r = s.get(capt_url)
    print(r.content)
    content = str(r.content)
    if "show_captcha" in content:
        print ('false')
        return None
    print ("获取验证码图片状态："+str(r.status_code))
    with open("zhuhu.png","wb") as f:
        f.write(r.content)
    a = input("请输入倒立的文字的x坐标：") #范围[0-200].比如：20,100,150
    x_nums = a.split(',')
    input_points = [[int(x),20] for x in x_nums]
    return input_points

if __name__ == "__main__":
    # x = get_xsrf()
    # print(x)
    # input_points = get_capt()
    # print (input_points)
    login()
