# -*- coding:utf-8 -*-

import time,pymysql,sys,random,re,os
reload(sys)
sys.setdefaultencoding('utf8')

conn = pymysql.connect(host='122.224.129.35', port=23306, user='repository', passwd='repository', db='repository',charset='utf8')
cur = conn.cursor()
cur.execute("SELECT url,Main_body FROM repository.weixin_info where Main_body like '%picture_hzz%'")
rows = cur.fetchall()
for row in rows:
    context = row[1].replace('/picture_hzz/','http://122.224.129.35:28080/picture_hzz/')
    cur.execute("update website set context = %s where url = %s",(context,row[0]))
    print context
    conn.commit()
# if len(rows) == 0:
#     try:
#         sql = 'INSERT INTO website(url,title,push_time,context,come_from,page_type,type_id,spider_time,source) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         # 批量插入
#         cur.execute(sql,result)
#         conn.commit()
#     except Exception as e:
#         print e
#         conn.rollback()
# else:
#     result = result[::-1]
#     try:
#         sql = 'UPDATE website SET source=%s,spider_time=%s,type_id=%s,page_type=%s,come_from=%s,context=%s,push_time=%s,title=%s WHERE url=%s'
#         # 批量更新
#         cur.execute(sql,result)
#         conn.commit()
#     except Exception as e:
#         print e
#         conn.rollback()
# 释放数据连接
if cur:
    cur.close()
if conn:
    conn.close()