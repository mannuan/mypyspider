#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-18 09:06:44
# Project: weibo_hot_comment

from pyspider.libs.base_handler import *
import time, pymysql,re
from lxml import html

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
    }

    @every(minutes=12 * 60)#12小时
    def on_start(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        # 先查找是否存在
        sql = "select note_url,note_id from note where note_url like %s"
        cur.execute(sql,"https://m.weibo.cn/api/comments/show?id=%")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        for row in rows:
            url = row[0]#热门评论都在第一页
            note_id = row[1]
            weibo_id = url.split('&')[0].split('=')[-1]
            # print url,weibo_id,note_id
            self.crawl(url, callback=self.index_page,save={'weibo_id':weibo_id,'note_id':note_id})

    @config(age=12 * 60 * 60)#12小时
    def index_page(self, response):
        ob_json = response.json
        list_comments = ob_json.get('hot_data')
        if list_comments is None:
            list_comments = ob_json.get('data')
            if list_comments is None:
                return
            elif len(list_comments) >=9:
                list_comments = list_comments[0:9]
        result = []
        for comment in list_comments:
            user_id = comment.get('user').get('id')  # 发表评论者的id
            user_name = comment.get('user').get('screen_name')  # 发表评论者的昵称
            weibo_id = response.save['weibo_id']#评论所对应的微博的id
            note_id = response.save['note_id']
            comment_id = comment.get('id')#评论的id
            created_at = comment.get('created_at')#创建的时间
            source = comment.get('source')  # 来自那个哪个设备
            if source == '':
                source = u'未知'
            text = comment.get('text')
            tree = html.fromstring(text)
            text = tree.xpath('string(.)')  # 微博内容,用string函数过滤多余标签
            like_counts = comment.get('like_counts')  # 点赞数
            crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))#爬虫的时间
            result.append([note_id,comment_id,text,created_at,crawl_time,user_id])
        # print result
        return result

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        try:
            sql = 'REPLACE INTO note_comment values(%s,%s,%s,%s,%s,%s)'
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