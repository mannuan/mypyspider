#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-17 16:16:52
# Project: weibo_user

from pyspider.libs.base_handler import *
import time, pymysql

class Handler(BaseHandler):
    @every(minutes=24*60)#一天
    def on_start(self):
        for i in range(1, 31):
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={}'.format(i)
            self.crawl(url, callback=self.index_page)

    @config(age=24*60*60)#单位:秒,一天
    def index_page(self, response):
        ob_json = response.json
        list_cards = ob_json.get('cards')
        if list_cards is None:
            return
        result = []
        for card in list_cards:
            if card.get('card_type') is 9:
                user_id = card.get('mblog').get('user').get('id')
                user_name = card.get('mblog').get('user').get('screen_name')
                user_verified_reason = card.get('mblog').get('user').get('verified_reason')
                if user_verified_reason is None:
                    user_verified_reason = u'未认证'
                crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                result.append([user_id,user_name,user_verified_reason,crawl_time])
        return result

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
        cur = conn.cursor()
        try:
            sql = 'INSERT INTO weibo_user(user_id,user_name,user_verified_reason,crawl_time) values(%s,%s,%s,%s)'
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