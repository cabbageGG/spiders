#-*- coding: utf-8 -*-

# author: li yangjin

import requests
import re
from fake_useragent import UserAgent
import json

ua = UserAgent()
User_Agent = ua.random
headers = {
    "User-Agent":User_Agent
}

s = requests.session()
s.headers = headers
def get_xsrf():
    url = "https://www.zhihu.com"
    r = s.get(url)
    pattern = re.compile(r'.*name="_xsrf" value="(.*?)"')
    match = re.findall(pattern, r.text)
    if match:
        _xsrf = match[0]
    else:
        _xsrf = ""
    return _xsrf

def login():
    _xsrf = get_xsrf()
    login_url = "https://www.zhihu.com/login/phone_num"
    # captcha:{"img_size":[200,44],"input_points":[[118.667,24.2708],[166.667,22.2708]]}
    # 大约连续输入错误密码5次，出现倒立文字校验码。
    input_points = get_capt()
    captcha = {"img_size":[200,44],"input_points":input_points}
    captcha_str = json.dumps(captcha)
    post_data = {
        "_xsrf":_xsrf,
        "phone_num":"13246856469",
        "password":"******",
        "captcha_type":"cn",
         "captcha":captcha_str
    }
    r = s.post(login_url, data=post_data)

    print ("登录请求状态："+str(r.status_code))
    ret_json = json.loads(r.text, encoding='utf-8')
    msg = ret_json.get("msg","")
    print ("登录返回结果："+msg)


def get_capt():
    capt_url = "https://www.zhihu.com/captcha.gif?type=login&lang=cn"
    r = s.get(capt_url)
    print ("获取验证码图片状态："+str(r.status_code))
    with open("zhuhu.png","wb") as f:
        f.write(r.content)
    a = input("请输入倒立的文字的x坐标：") #范围[0-200].比如：20,100,150
    x_nums = a.split(',')
    input_points = [[x,20] for x in x_nums]
    return input_points

if __name__ == "__main__":
    # x = get_xsrf()
    # print(x)
    # input_points = get_capt()
    # print (input_points)
    login()
