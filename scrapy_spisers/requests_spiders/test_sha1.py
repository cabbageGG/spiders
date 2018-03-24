#-*- coding: utf-8 -*-

import hmac
from hashlib import sha1

'''
6035da5749cfc96da1a316452a1a8e865eb4b06b
'''

client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
grant_type = 'password'
timestamp = '1516267147031'
source = 'com.zhihu.web'
key = b'd1b964811afb40118a12068ff74a12f4'

h = hmac.new(key,digestmod=sha1)
h.update(grant_type.encode('utf-8'))
h.update(client_id.encode('utf-8'))
h.update(source.encode('utf-8'))
h.update(timestamp.encode('utf-8'))
print(h.hexdigest())
