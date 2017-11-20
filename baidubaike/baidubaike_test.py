# -*- coding:utf-8 -*-

import urllib2,random,sys,re,time,json
reload(sys)
sys.setdefaultencoding('utf8')

url = "https://m.weibo.cn/status/4176079084453621"
headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"]
random_header = random.choice(headers)
req =urllib2.Request(url)
req.add_header("User-Agent", random_header)
req.add_header("GET",url)
text=urllib2.urlopen(req).read()
hjson = json.loads(text)
print hjson
# f = open('temp.html','w+')
# f.write(text)
# f.close()
# from pyquery import PyQuery
# p = PyQuery(text)
# for each in p('a[href^="http"]').items():
#     print each.attr.href