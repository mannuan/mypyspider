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

    list_forums = [{'forum':'0bj6','page':5,'name':u'综合动态','type':u'动态'},
                   {'forum':'0bj7','page':13,'name':u'地方动态','type':u'动态'},
                   {'forum':'0bj9','page':2,'name':u'经验交流','type':u'动态'}]

    @every(minutes=24 * 60)
    def on_start(self):
        url = "http://www.zjwater.com/pages/category/0bja/index_1.htm"
        self.crawl(url, fetch_type='js', callback=self.index_page1,
                   save={'name': u"政策文件,2015年11月10日起", 'type': u"政府发文"})
        # for forum in self.list_forums:
        #     for p in range(1,forum.get('page')+1):
        #         url = 'http://www.zjwater.com/pages/category/{}/index_{}.htm'.format(forum.get('forum'),p)
        #         self.crawl(url, fetch_type='js', callback=self.index_page,save={'name':forum.get('name'),'type':forum.get('type')})

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('table#ctl00_cphBody_ctl00_dt_itemlist>tbody>tr>td>table>tbody>tr').items():
            url = each('td>div.SHORT_DIV1>a').attr.href
            title = each('td>div.SHORT_DIV1>a').attr.title
            created_at = each('td').text()
            name = response.save['name']
            type = response.save['type']
            # print url,title,created_at,name,type
            self.crawl(url, fetch_type='js', callback=self.detail_page, save={'title':title,'created_at':created_at,'name':name,'type':type})

    @config(age=10 * 24 * 60 * 60)
    def index_page1(self, response):
        for each in response.doc('table#ctl00_cphBody_ctl00_dt_itemlist>tbody>tr>td>table>tbody>tr').items():
            url = each('td>div.SHORT_DIV1>a').attr.href
            title = each('td>div.SHORT_DIV1>a').attr.title
            created_at = each('td').text()
            name = response.save['name']
            type = response.save['type']
            # print url,title,created_at,name,type
            print type(created_at)
            # timeStamp1 = int(time.mktime(time.strptime("2015.11.10", "%Y.%m.%d")))
            # timeStamp2 = int(time.mktime(time.strptime(created_at, "%Y.%m.%d")))
            # if timeStamp2 > timeStamp1:
            #     self.crawl(url, fetch_type='js', callback=self.detail_page,
            #            save={'title': title, 'created_at': created_at, 'name': name, 'type': type})

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        title = response.save['title']
        created_at = response.save['created_at']
        text = ''
        for cs in ['td#NewsContent>p','table.MsoNormalTable>tbody>tr>td>p']:
            for each in response.doc(cs).items():
                text += each.text()
            if text is not '':
                break
        come_from = response.doc('td#NewsContent>div').text().split(u'发布时间')[0].replace(u'来源：','')
        if come_from is None:
            come_from = text.split(u'来源：')[-1]
        forum_name = response.save['name']
        forum_type = response.save['type']
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
        result = [url,title,created_at,text,come_from,forum_name,type_id,crawl_time,u'浙江省水利厅/五水共治']
        # print text
        # print come_from
        # print type_id
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
                sql = 'INSERT INTO website(url,title,push_time,context,come_from,page_type,type_id,spider_time,source) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                # 批量插入
                cur.execute(sql,result)
                conn.commit()
            except Exception as e:
                print e
                conn.rollback()
        else:
            result = result[::-1]
            try:
                sql = 'UPDATE website SET source=%s,spider_time=%s,type_id=%s,page_type=%s,come_from=%s,context=%s,push_time=%s,title=%s WHERE url=%s'
                # 批量更新
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