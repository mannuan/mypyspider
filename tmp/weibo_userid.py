# -*- coding:utf-8 -*-
import requests,json,re

page=1
while True:
    url = "https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={}".format(page)
    reponse = requests.get(url)
    ob_json = json.loads(reponse.text)
    list_cards = ob_json.get('cards')
    if len(list_cards) is 0:
        break
    for card in list_cards:
        mblog = card.get('mblog')
        user = mblog.get('user')
        id = user.get('id')
        screen_name = user.get('screen_name')
        print id,screen_name


