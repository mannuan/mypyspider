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

    list_forums = [{'forum':'policy','page':429,'name':u'政策文件','type':u'政府发文'},
                   {'forum':'law','page':47,'name':u'法律法规','type':u'政府发文'},
                   {'forum':'standard','page':64,'name':u'标准规范','type':u'标准'}]

    list_text_css_selector = ['td.content>div.TRS_Editor>p','div.model#about_txt>div.mbd>div.cnt_bd>p','div.slnewscon.autoHeight','div.vintro>p','div.content1']

    @every(minutes=24 * 60)
    def on_start(self):
        for forum in self.list_forums:
            for p in range(1,forum.get('page')+1):
                url = 'http://www.h2o-china.com/{}/home?ordby=dateline&sort=DESC&page={}'.format(forum.get('forum'),p)
                self.crawl(url, fetch_type='js', callback=self.index_page,save={'forum':forum.get('forum'),'name':forum.get('name'),'type':forum.get('type')})

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.lists.txtList>ul>li').items():
            url = each('em.title>a.ellip.w540.i-pdf').attr.href
            file_format = 'pdf'
            if url is None:
                url = each('em.title>a.ellip.w540.i-word').attr.href
                file_format = 'doc'
                if url is None:
                    url = each('em.title>a.ellip.w540.0').attr.href
                    file_format = None
            forum = response.save['forum']
            name = response.save['name']
            type = response.save['type']
            self.crawl(url, fetch_type='js', callback=self.detail_page, save={'forum':forum,'name':name,'type':type,'file_format':file_format})

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        title = response.doc('div.hd>h1').text()
        file_type = response.doc('div.traits>table>tbody>tr:nth-child(1)>td:nth-child(2)').text()
        created_at = response.doc('div.traits>table>tbody>tr:nth-child(1)>td:nth-child(4)').text()
        dispatch_unit = response.doc('div.traits>table>tbody>tr:nth-child(2)>td:nth-child(2)').text()
        file_number = response.doc('div.traits>table>tbody>tr:nth-child(3)>td:nth-child(2)').text()
        key_words = response.doc('div.traits>table>tbody>tr:nth-child(4)>td:nth-child(2)').text()
        abstract = response.doc('div.traits>table>tbody>tr:nth-child(5)>td:nth-child(2)').text()
        forum_name = response.save['name']
        forum_type = response.save['type']
        file_name = url.split('/')[-1].replace('.html','')+'.'+response.save['file_format']
        file_url = 'http://www.h2o-china.com/{}/view/download?id={}'.format(response.save['forum'],url.split('/')[-1].replace('.html',''))
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
        result = []
        result.append([url,title,file_type,created_at,dispatch_unit,file_number,key_words,abstract,forum_name,type_id,file_name,file_url,crawl_time])
        return result

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        try:
            sql = 'REPLACE INTO zhongguoshuiwang values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            # 批量插入
            cur.executemany(sql,result)
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
        # 释放数据连接
        if cur:
            cur.close()
        if conn:
            conn.close()