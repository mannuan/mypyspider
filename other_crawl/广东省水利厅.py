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

    list_forums1 = [{'forum':'/slzc/szygl/','page':1,'name':u'政策法规/水资源管理,中央','type':u'政府发文'},
                   {'forum':'/slfl/','page':1,'name':u'政策法规/水利法律,中央','type':u'政府发文'},
                   {'forum':'/xzfg/','page':1,'name':u'政策法规/水利行政法规,中央','type':u'政府发文'},
                   {'forum':'/dfxfg/','page':1,'name':u'政策法规/广东省地方性水事法规,广东省','type':u'政府发文'},
                   {'forum':'/bsgz/','page':1,'name':u'政策法规/广东省人民政府水事规章,广东省','type':u'政府发文'},
                   {'forum':'/bwgz/bwgzszygl/','page':1,'name':u'政策法规/水资源管理,中央','type':u'政府发文'},
                   {'forum':'/bwgz/stbcgl/','page':1,'name':u'政策法规/水土保持管理,中央','type':u'政府发文'},
                   {'forum':'/bwgz/swgl/','page':1,'name':u'政策法规/水文管理,中央','type':u'政府发文'},
                   {'forum':'/qtfg/','page':1,'name':u'其他水事法规规章性文件,广东省/中央','type':u'政府发文'}]

    list_forums2 = [{'forum':'mtgz','page':100,'name':u'媒体关注','type':u'动态'},
                   {'forum':'qgss','page':81,'name':u'全国水事','type':u'动态'}]

    list_text_css_selector = ['td.content>div.TRS_Editor>p','div.model#about_txt>div.mbd>div.cnt_bd>p','div.slnewscon.autoHeight','div.vintro>p','div.content1']

    @every(minutes=24 * 60)
    def on_start(self):
        # for forum in self.list_forums1:
        #     url = 'http://www.gdwater.gov.cn/xxgk/wjzy/zcfg{}list.htm'.format(forum.get('forum'))
        #     self.crawl(url, fetch_type='js', callback=self.index_page,save={'name':forum.get('name'),'type':forum.get('type')})
        for forum in self.list_forums2:
            url = 'http://www.gdwater.gov.cn/yszx/slyw/{}/index.html'.format(forum.get('forum'))
            self.crawl(url, fetch_type='js', callback=self.index_page1,
                       save={'name': forum.get('name'), 'type': forum.get('type')})
            for p in range(1,forum.get('page')):
                url = 'http://www.gdwater.gov.cn/yszx/slyw/{}/index_{}.html'.format(forum.get('forum'),p)
                self.crawl(url, fetch_type='js', callback=self.index_page1,
                           save={'name': forum.get('name'), 'type': forum.get('type')})

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.row').items():
            url = each('li.mc>div>a').attr.href
            title = each('li.mc>div>a').text()
            created_at = each('li.fbrq').text()
            name = response.save['name']
            type = response.save['type']
            # print url,title,created_at,name,type
            self.crawl(url, fetch_type='js', callback=self.detail_page, save={'title':title,'created_at':created_at,'name':name,'type':type})

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        title = response.save['title']
        created_at = response.save['created_at']
        release_mechanism = response.doc('div.headInfo>table#headContainer>tbody>tr:nth-child(2)>td>table>tbody>tr>td:nth-child(1)>span').text()
        text = ''
        for each in response.doc('div.mainContainer>div#ContentRegion.content>p').items():
            text += each.text()
        file_url = response.doc('div.mainContainer>div#ContentRegion.content>p>a').attr.href
        file_name = None
        if file_url is not None:
            file_name = file_url.split('/')[-1]
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
        # print release_mechanism,text,forum_type,type_id,file_url,file_name
        result = [url,title,created_at,release_mechanism,text,file_url,file_name,forum_name,type_id,crawl_time,u'广东省水利厅']
        return result

    @config(age=24 * 60 * 60)
    def index_page1(self, response):
        for each in response.doc('div.gl-right>ul.gl-list>li').items():
            url = each('a').attr.href
            # title = each('a').text()
            created_at = each('span').text()
            name = response.save['name']
            type = response.save['type']
            # print url,title,created_at,name,type
            self.crawl(url, fetch_type='js', callback=self.detail_page1,
                       save={'created_at': created_at, 'name': name, 'type': type})

    @config(priority=2)
    def detail_page1(self, response):
        url = response.url
        title = response.doc('div.xlbox>h4').text()
        created_at = response.save['created_at']
        come_from = response.doc('div.xlbox>h5>label:nth-child(1)').text()
        if come_from is not None:
            come_from = come_from.replace('来源：','')
        text = ''
        for each in response.doc('div.xl-nr>div>div>div.Custom_UnionStyle>p').items():
            text += each.text()
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
        # print release_mechanism,text,forum_type,type_id,file_url,file_name
        result = [url,title,created_at,release_mechanism,text,file_url,file_name,forum_name,type_id,crawl_time,u'广东省水利厅']
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
                sql = 'INSERT INTO website(url,title,push_time,come_from,context,file_url,file_name,page_type,type_id,spider_time,source) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                # 批量插入
                cur.execute(sql,result)
                conn.commit()
            except Exception as e:
                print e
                conn.rollback()
        else:
            result = result[::-1]
            try:
                sql = 'UPDATE website SET source=%s,spider_time=%s,type_id=%s,page_type=%s,file_name=%s,file_url=%s,context=%s,come_from=%s,push_time=%s,title=%s WHERE url=%s'
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