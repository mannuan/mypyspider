#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 22:49:57 2018

@author: mannuan
"""

import re,binascii,zlib

with open('/home/mininet/bk_before_content','r') as f:
    content = f.read().strip()
    f.close()
regex = re.compile(r'(<)[^\/\s\"\=>]+(\s+)(?!href)[^\s\"]+(\s*=\s*?\")((?=https://|http://)[^\">]+?)(\"\s*/>)')
url_list = [i[3] for i in regex.findall(content)]
result = regex.sub(r'\1img\2src\3\4\5',content)
for url in url_list:
    h = binascii.b2a_hex(url)
    print h
    # print binascii.a2b_base64(h)
    # c = binascii.crc32(url)
    # print binascii.crc_hqx(url)
# print result