#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-20 13:26:05
# Project: weibo_user_test

from pyspider.libs.base_handler import *
import time,pymysql,re

class Tool:
    #去除img标签
    removeImg = re.compile('<img.*>| {1,7}|&nbsp;')
    #去除超链接 a标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行换成\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')

    #去除所有标签
    removeTag = re.compile('<.*?>')

    @classmethod
    def replace(cls,x):
        x = re.sub(cls.removeImg,'',x)
        x = re.sub(cls.removeAddr,'',x)
        x = re.sub(cls.replaceLine,'',x)
        x = re.sub(cls.removeTag,'',x)

        return x.strip()#去掉多余的内容

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

    key_words = ["河长制", "智慧治水", "水利厅", "污水治理", "一河一策", "水政执法", "水资源保护", "河湖水域岸线保护", "水污染防治", "水生态修复", "水利工程管理", "环境改善","水质监测", "涉河水利工程", "岸线规划", "污水治理", "水环境治理"]

    @every(minutes=12 * 60)
    def on_start(self):
        for kw in self.key_words:
            url = 'http://s.weibo.com/weibo/{}'.format(kw)
            self.crawl(url, fetch_type='js', callback=self.index_page)

    @config(age=12 * 60 * 60)
    def index_page(self, response):
        result = []
        for each in response.doc('div').items():
            user_id = each.attr.tbinfo
            user_name = each('div.WB_feed_detail.clearfix > dl > div > div.content.clearfix > div.feed_content.wbcon > a.W_texta.W_fb').attr.title
            weibo_id = each.attr.mid
            created_at = each('div.WB_feed_detail.clearfix > dl > div > div.content.clearfix > div.feed_from.W_textb > a.W_textb').text()
            source = each('div.WB_feed_detail.clearfix > dl > div > div.content.clearfix > div.feed_from.W_textb > a:nth-child(2)').text()
            if user_id and user_name and weibo_id and created_at and source:
                user_id = user_id.replace('ouid=','')#微博用户的id
                url = "https://m.weibo.cn/statuses/extend?id={}".format(weibo_id)
                self.crawl(url, callback=self.detail_page, save={'user_id':user_id,'user_name':user_name,'weibo_id':weibo_id,'created_at':created_at,'source':source})

    @config(priority=2)
    def detail_page(self, response):
        result = []
        ob_json = response.json
        user_id = response.save['user_id']
        user_name = response.save['user_name']
        weibo_id = response.save['weibo_id']
        created_at = response.save['created_at']
        source = response.save['source']
        longTextContent = Tool.replace(ob_json.get('longTextContent'))
        reposts_count = ob_json.get('reposts_count')
        comments_count = ob_json.get('comments_count')
        attitudes_count = ob_json.get('attitudes_count')
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬虫的时间
        result.append([user_id,user_name,weibo_id,created_at,source,longTextContent,reposts_count,comments_count,attitudes_count,crawl_time])
        return result

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        try:
            sql = 'REPLACE INTO weibo_weibo values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
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