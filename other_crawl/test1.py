#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-21 16:41:40
# Project:

from pyspider.libs.base_handler import *
import time,pymysql,sys
reload(sys)
sys.setdefaultencoding('utf8')

conn = pymysql.connect(host='122.224.129.35', port=23306, user='repository', passwd='repository', db='repository',charset='utf8')
cur = conn.cursor()
try:
    sql = 'select url from website where source = \'浙江省环保厅\' and context like \'%<p>%\';'
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print row[0]
    print len(rows)
    # sql = 'delete from website where url = %s'
    # cur.executemany(sql,rows)
    # conn.commit()
except Exception as e:
    print e
    conn.rollback()
# 释放数据连接
if cur:
    cur.close()
if conn:
    conn.close()