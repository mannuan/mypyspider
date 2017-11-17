# -*- coding:utf-8 -*-

import requests,json,time,pymysql

class Handler(object):

    # @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 31):
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={}'.format(i)
            response = requests.get(url)
            ob_json = json.loads(response.text)
            list_cards = ob_json.get('cards')
            self.get_user(list_cards)

    # @config(priority=2)
    def get_user(self,list_cards):
        for card in list_cards:
            if card.get('card_type') is 9:
                user_id = card.get('mblog').get('user').get('id')
                user_name = card.get('mblog').get('user').get('screen_name')
                user_verified_reason = card.get('mblog').get('user').get('verified_reason')
                if user_verified_reason is None:
                    user_verified_reason = u'未认证'
                crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                result = {'user_id':user_id,'user_name':user_name,'user_verified_reason':user_verified_reason,
                          'crawl_time':crawl_time}
                # return result
                self.on_result(result)

    def on_result(self,result):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository',
                               db='repository',
                               charset='utf8')
        cur = conn.cursor()
        # 先查找是否存在
        cur.execute("select * from weibo_user where user_id = %s", result['user_id'])
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute(
                "insert into weibo_user(user_id,user_name,user_verified_reason,crawl_time) values(%s,%s,%s,%s)",
                (result['user_id'], result['user_name'], result['user_verified_reason'], result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
    handler = Handler()
    handler.on_start()