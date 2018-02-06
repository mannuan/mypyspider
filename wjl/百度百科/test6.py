# -*- coding:utf-8 -*-
import pymysql,json

conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
cur = conn.cursor()
cur.execute("select name from river")
rows = cur.fetchall()
conn.commit()
cur.close()
conn.close()
river_list = [i[0].encode('utf-8') for i in rows]
with open('/home/mininet/baidubaike.txt','w+') as f:
    f.write(json.dumps(river_list,ensure_ascii=False))