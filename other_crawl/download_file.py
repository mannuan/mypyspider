# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
cur = conn.cursor()
try:
    cur.execute("select file_name,file_url from website where file_url like '%.%'")
    rows = cur.fetchall()
    conn.commit()
except Exception as e:
    conn.rollback()
    print e
if cur:
    cur.close()
if conn:
    conn.close()
import os,requests
file_name_list = []
for row in rows:
    r = requests.get(row[1], stream=True)
    file_name = os.getcwd()+'/website_document/'+row[0]
    f = open(file_name, "wb+")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    file_name_list.append(file_name)
conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
cur = conn.cursor()
try:
    sql = "UPDATE website set file_name = %s"
    cur.executemany(sql,file_name_list)
    conn.commit()
except Exception as e:
    conn.rollback()
    print e
if cur:
    cur.close()
if conn:
    conn.close()