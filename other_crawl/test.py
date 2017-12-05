#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:36:17 2017

@author: mininet
"""

import pymysql

conn = pymysql.connect(host='122.224.129.35', port=23306, user='repository', passwd='repository', db='repository',
                       charset='utf8')
cur = conn.cursor()
cur.execute("select url from website where source = '浙江省水利厅/五水共治' and file_name != ''")
rows = cur.fetchall()
# 释放数据连接
if cur:
    cur.close()
if conn:
    conn.close()
for row in rows:
    sql = "update website set file_name = '',file_url = '' where url = %s"
    conn = pymysql.connect(host='122.224.129.35', port=23306, user='repository', passwd='repository', db='repository',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute(sql,row[0])
    conn.commit()
    # 释放数据连接
    if cur:
        cur.close()
    if conn:
        conn.close()
    print row[0]
