#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-21 14:28:38
# Project: baidubaike

from pyspider.libs.base_handler import *
import pymysql,time
import sys,re
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf-8')

class Handler(BaseHandler):
    crawl_config = {
        "headers":{
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Upgrade-Insecure-Requests':'1',
            'Content-Encoding': 'gzip',
            'Content-Type': 'text/html',
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("select name from river")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        for row in rows:
            url = u'http://wapbaike.baidu.com/item/{}'.format(row[0])
            self.crawl(url, save={'river_name':row[0]}, callback=self.index_page)

    def filter_page(self,response,*args):
        content = ''
        for cs in args:
            rd = response.doc(cs)#rd是一个PyQuery对象
            rd('script').remove()
            rd('style').remove()
            content += (lambda x:'' if x is None else re.sub(r'(\s+[^\s\"]+\s*=\s*?\"(?!https://|http://)[^\">]+?\")|[\f\n\r]+', '', x))(rd.html())
        regex = re.compile(r'(<)[^\/\s\"\=>]+(\s+)(?!href)[^\s\"]+(\s*=\s*?\")((?=https://|http://)[^\">]+?)(\"\s*/>)')
        content = regex.sub(r'\1img\2src\3\4\5', content)
        url_list = [i[3] for i in regex.findall(content)]
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("select id from localpicture")
        maxid = (lambda x:0 if x is None else x[0])(cur.fetchone())
        cur.executemany("insert into localpicture(url) values(%s)",url_list)
        conn.commit()
        cur.close()
        conn.close()
        for i in range(len(url_list)):
            content.replace(url_list[i],str(maxid+i+1))
        return content

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        river_name = response.save['river_name']
        url = response.url
        content = self.filter_page(response,
                         '#J-lemma > div.BK-body-wrapper > div.BK-before-content-wrapper',
                         '#J-lemma > div.BK-body-wrapper > div.BK-content-wrapper')
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬虫的时间
        return [content,crawl_time,river_name,url]

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        try:
            sql = 'REPLACE INTO baidubaike values(%s,%s,%s,%s)'
            # 批量插入
            cur.execute(sql,result)
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
        # 释放数据连接
        if cur:
            cur.close()
        if conn:
            conn.close()