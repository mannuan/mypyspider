# -*- coding:utf-8 -*-

from pyquery import PyQuery as py
import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('/home/mannuan/content.html') as f:
    content = f.read().decode('utf-8')
    f.close()
p = py(content)
print p.removeAttr('style')
