# -*- coding:utf-8 -*-
import requests,json,time,pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository',
                       db='repository',
                       charset='utf8')
cur = conn.cursor()
# 先查找是否存在
cur.execute("select user_id from weibo_user")
rows = cur.fetchall()
for id in rows:
    print id[0]
conn.commit()
cur.close()
conn.close()