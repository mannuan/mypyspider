# -*- coding:utf-8 -*-

# https://m.weibo.cn/p/102803_ctg1_8999_-_ctg1_8999_home

import requests,json,re
import sys,time,pymysql

page=1
while True:
    url = "https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={}".format(page)
    page+=1
    reponse = requests.get(url)
    ob_json = json.loads(reponse.text)
    list_cards = ob_json.get('cards')
    if len(list_cards) is 0:
        break
    for card in list_cards:
        if card.get('card_type') is 9:
            mblog = card.get('mblog')
            user = mblog.get('user')
            id = user.get('id')
            screen_name = user.get('screen_name')
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='sdn', db='repository',
                                   charset='utf8')
            cur = conn.cursor()
            cur.execute("insert into weibo_user(uid,uname) values(%s,%s)",(id, screen_name))
            conn.commit()
            cur.close()
            conn.close()