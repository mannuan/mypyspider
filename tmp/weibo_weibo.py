#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-17 16:16:52
# Project: weibo_user

from pyspider.libs.base_handler import *
import requests, json, time, pymysql,re
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

    @every(minutes=24 * 60)
    def on_start(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
        cur = conn.cursor()
        # 先查找是否存在
        cur.execute("select user_id from weibo_user")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        for id in rows:
            url = "https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}&page={}".format(id[0], id[0], id[0], 1)
            self.crawl(url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        ob_json = response.json
        list_cards = ob_json.get('cards')
        for card in list_cards:  # 遍历
            if card.get('card_type') == 9:#等于9的微博才是正文,其他的都是推荐或者其他,`weibo_user`的唯一标识
                mblog_user_id = card.get('mblog').get('user').get('id')#微博用户的id
                mblog_user_name = card.get('mblog').get('user').get('screen_name')#微博用户的昵称
                mblog_user_verified_reason = card.get('mblog').get('user').get('verified_reason')
                if mblog_user_verified_reason is None:
                    mblog_user_verified_reason = u'未认证'
                mblog_id = card.get('mblog').get('id')#微博的id,`weibo_weibo`table的唯一标识
                mblog_created_at = card.get('mblog').get('created_at')#微博创建的时间
                mblog_source = card.get('mblog').get('source')#微博的来源
                if mblog_source == '':
                    mblog_source = u'未知'
                mblog_text = card.get('mblog').get('text')
                mblog_text = Tool.replace(mblog_text)#微博的内容
                mblog_reposts_count = card.get('mblog').get('reposts_count')#微博的转发数
                mblog_comments_count = card.get('mblog').get('comments_count')#微博的评论数
                mblog_attitudes_count = card.get('mblog').get('attitudes_count')#微博的点赞数
                crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository',
                                       db='repository', charset='utf8')
                cur = conn.cursor()
                # 先查找是否存在
                cur.execute("select * from weibo_user where user_id = %s", mblog_user_id)
                rows = cur.fetchall()
                if len(rows) == 0:
                    cur.execute(
                        "insert into weibo_user(user_id,user_name,user_verified_reason,crawl_time) values(%s,%s,%s,%s)",
                        (user['user_id'], user['user_name'], user['user_verified_reason'], user['crawl_time']))
                    conn.commit()
                    cur.close()
                    conn.close()

                if len(mblog_text) is 0:#如果发表的微博里面没有文字,继续
                    continue



                url = "https://m.weibo.cn/api/comments/show?id={}&page={}".format(mblog_id,1)
                self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        ob_json = response.json
        list_comments = ob_json.get('hot_data')
        if list_comments is None:
            list_comments = ob_json.get('data')
            if list_comments is None:
                pass
            elif len(list_comments) >=9:
                list_comments = list_comments[0:9]
        for comment in list_comments:
            comment_user_id = comment.get('user').get('id')  # 发表评论者的id
            comment_user_name = comment.get('user').get('screen_name')  # 发表评论者的昵称
            comment_created_at = comment.get('created_at')  # 创建的时间
            comment_like_counts = comment.get('like_counts')  # 点赞数
            comment_text = comment.get('text')
            tree = html.fromstring(comment_text)
            comment_text = tree.xpath('string(.)')  # 微博内容,用string函数过滤多余标签
            comment_source = comment.get('source')  # 来自那个哪个设备
            if comment_source == '':
                comment_source = u'未知'


    def on_result(self, result):
        pass