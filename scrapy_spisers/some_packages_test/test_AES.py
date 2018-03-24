#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/18 11:20'

from Cryptodome.Cipher import AES
import base64
import math

# 将字符串转换成二进制的buff块
def parse_hex(hex_str):
    l=int(math.ceil(len(hex_str)/2))
    buf=''
    for i in range(0,l):
        s=hex_str[(i*2):((i+1)*2)]
        buf=buf+chr(int(s,16))
    return buf

# 解析加密的key
key=parse_hex("68b329da9893e34099c7d8ad5cb9c940")
iv=parse_hex("68b329da9893e34099c7d8ad5cb9c940")

from Cryptodome.Random import get_random_bytes

key = get_random_bytes(16)
e = AES.new(key, AES.MODE_CBC)

# e = AES.new(b'111123412345rerther3454',AES.MODE_CBC,b"234567u3456")
test = b'test'
pad = 16 - len(test) % 16
a = pad * b'0'
test = test + a
print(test)
enc_text = e.encrypt(test)
print (enc_text)
enc_text1 = base64.b64encode(enc_text)
print (enc_text1)
e1 = AES.new(key, AES.MODE_CBC)
dec_text = e1.decrypt(enc_text)
print (dec_text)
dec_text1 = base64.b64encode(dec_text)
print (dec_text1)