# -*- coding:utf-8 -*-
import time,json,pymysql,os

conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',
                       charset='utf8')
cur = conn.cursor()
cur.execute("select * from weixin_public")
rows = cur.fetchall()
conn.commit()
cur.close()
conn.close()
print rows