#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-21 16:41:40
# Project:

from pyspider.libs.base_handler import *
import time,pymysql,sys
reload(sys)
sys.setdefaultencoding('utf8')

class Handler(BaseHandler):
    crawl_config = {
        "headers":{
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Accept": "*/*",
        "DNT": "1",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
    }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        forum = {'name':u'信息公开/环保动态','page':10,'type':u'动态'}
        for p in range(1,forum.get('page')+1):
            url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?texttype=0&fbtime=-1&infotypeId=A001D001&jdid=1756&divid=div1201347&currpage={}'.format(p)
            self.crawl(url, fetch_type='js', callback=self.index_page,save={'name':forum.get('name'),'type':forum.get('type')})

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('tr.tr_main_value_odd').items():
            url = each('td:nth-child(1)>a').attr.href
            title = each('td:nth-child(1)>a').attr.title
            created_at = each('td:nth-child(2)').text()
            name = response.save['name']
            type = response.save['type']
            self.crawl(url, fetch_type='js', callback=self.detail_page, save={'name':name,'type':type})

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        title = response.doc('div.hd>h1').text()
        file_type = response.doc('div.traits>table>tbody>tr:nth-child(1)>td:nth-child(2)').text()
        created_at = response.doc('div.traits>table>tbody>tr:nth-child(1)>td:nth-child(4)').text()
        dispatch_unit = response.doc('div.traits>table>tbody>tr:nth-child(2)>td:nth-child(2)').text()
        key_words = response.doc('div.traits>table>tbody>tr:nth-child(4)>td:nth-child(2)').text()
        abstract = response.doc('div.traits>table>tbody>tr:nth-child(5)>td:nth-child(2)').text()
        forum_name = response.save['name']
        forum_type = response.save['type']
        file_id = url.split('/')[-1].replace('.html','')
        file_format = response.save['file_format']
        file_name = file_id+'.'+file_format
        file_url = 'http://www.h2o-china.com/{}/view/download?id={}'.format(response.save['forum'],file_id)
        type_id = None
        conn = pymysql.connect(host='localhost', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("select id from type where name=%s", forum_type)
            row = cur.fetchone()
            type_id = row[0]
            conn.commit()
        except Exception as e:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))#爬虫的时间
        result = [url,title,created_at,dispatch_unit,abstract,forum_name,type_id,file_name,file_url,crawl_time,u'中国水网']
        return result

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from website where url = %s" , result[0])
        rows = cur.fetchall()
        if len(rows) == 0:
            try:
                sql = 'INSERT INTO website(url,title,push_time,come_from,context,page_type,type_id,file_name,file_url,spider_time,source) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                # 批量插入
                cur.execute(sql,result)
                conn.commit()
            except Exception as e:
                print e
                conn.rollback()
        else:
            result = result[::-1]
            try:
                sql = 'UPDATE website SET source=%s,spider_time=%s,file_url=%s,file_name=%s,type_id=%s,page_type=%s,context=%s,come_from=%s,push_time=%s,title=%s WHERE url=%s'
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