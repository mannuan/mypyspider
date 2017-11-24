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

    list_forums = [{'forum':'/slzc/szygl/','page':1,'name':u'政策法规/水资源管理','type':u'政府发文'},{'forum':'/slfl/','page':1,'name':u'政策法规/水利法律','type':u'政府发文'},{'forum':'/xzfg/','page':1,'name':u'政策法规/水利行政法规','type':u'政府发文'},{'forum':'/dfxfg/','page':1,'name':u'政策法规/广东省地方性水事法规','type':u'政府发文'},{'forum':'/bsgz/','page':1,'name':u'政策法规/广东省人民政府水事规章','type':u'政府发文'},{'forum':'/bwgz/bwgzszygl/','page':1,'name':u'政策法规/水资源管理','type':u'政府发文'},{'forum':'/bwgz/stbcgl/','page':1,'name':u'政策法规/水土保持管理','type':u'政府发文'},{'forum':'/bwgz/swgl/','page':1,'name':u'政策法规/水文管理','type':u'政府发文'},{'forum':'/qtfg/','page':1,'name':u'其他水事法规规章性文件','type':u'政府发文'}]

    list_text_css_selector = ['td.content>div.TRS_Editor>p','div.model#about_txt>div.mbd>div.cnt_bd>p','div.slnewscon.autoHeight','div.vintro>p','div.content1']

    @every(minutes=24 * 60)
    def on_start(self):
        for forum in self.list_forums:
            url = 'http://www.gdwater.gov.cn/xxgk/wjzy/zcfg{}list.htm'.format(forum.get('forum'))
            self.crawl(url, fetch_type='js', callback=self.index_page,save={'name':forum.get('name'),'type':forum.get('type')})

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        pass
        # for each in response.doc('div.dbgxia>div.dbgshang>table.tbg>tbody>tr>td:nth-child(2)>table:nth-child(4)>tbody>tr>td>table:nth-child(2)>tbody>tr').items():
        #     url = each('td:nth-child(2)>a').attr.href
        #     title = each('td:nth-child(2)>a').text()
        #     created_at = each('td:nth-child(3)').text().replace('&nbsp;','')
        #     name = response.save['name']
        #     type = response.save['type']
        #     self.crawl(url, fetch_type='js', callback=self.detail_page, save={'title':title,'created_at':created_at,'name':name,'type':type})

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        title = response.save['title']
        created_at = response.save['created_at']
        text = ''
        for cs in self.list_text_css_selector:
            for each in response.doc(cs).items():
                text += each.text()
            if text is not '':
                break
        editor = response.doc('td.content>p').text().replace('责编：','')
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
        result = [url,title,created_at,text,editor,forum_name,type_id,crawl_time,u'水利部河长制']
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