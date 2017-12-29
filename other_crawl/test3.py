# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import requests

base_url = 'https://mmbiz.qpic.cn/mmbiz_jpg/qJickicXOV5OGsAwcl6tOsHF0BdU4YWO7GDnlEbjKMy4o0ayfPI8WCRIej6yd19R2Nch1NUEhy9QUqRG02fgpDpA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1'

r = requests.get(base_url)

# 注意下面的处理方式
if r.status_code == requests.codes.ok:
    with open('/home/mininet/m0.jpg', 'wb+') as fd:
        for chunk in r.iter_content(100):
            fd.write(chunk)