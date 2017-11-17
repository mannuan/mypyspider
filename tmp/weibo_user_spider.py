#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-17 16:16:52
# Project: weibo_user

from pyspider.libs.base_handler import *
import requests, json, time, pymysql

class Handler(BaseHandler):
    @every(minutes=24*60)
    def on_start(self):
        for i in range(1, 31):
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={}'.format(i)
            self.crawl(url, callback=self.index_page)

    @config(age=10*24*60*60)#单位:秒
    def index_page(self, response):
        ob_json = response.json
        list_cards = ob_json.get('cards')
        result = []
        for card in list_cards:
            if card.get('card_type') is 9:
                user_id = card.get('mblog').get('user').get('id')
                user_name = card.get('mblog').get('user').get('screen_name')
                user_verified_reason = card.get('mblog').get('user').get('verified_reason')
                if user_verified_reason is None:
                    user_verified_reason = u'未认证'
                crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                result.append({'user_id': user_id, 'user_name': user_name,'user_verified_reason':user_verified_reason,'crawl_time': crawl_time})
        return result

    def on_result(self, result):
        if not result:
            return
        for user in result:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository',db='repository',charset='utf8')
            cur = conn.cursor()
            # 先查找是否存在
            cur.execute("select * from weibo_user where user_id = %s", user['user_id'])
            rows = cur.fetchall()
            if len(rows) == 0:
                cur.execute("insert into weibo_user(user_id,user_name,user_verified_reason,crawl_time) values(%s,%s,%s,%s)",(user['user_id'], user['user_name'], user['user_verified_reason'], user['crawl_time']))
                conn.commit()
                cur.close()
                conn.close()