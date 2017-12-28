#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-21 16:41:40
# Project: weixin

host = "127.0.0.1"
port = 3306
user = "repository"
passwd = "repository"
db = 'repository'

from pyspider.libs.base_handler import *
import time,json,pymysql,os


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60 * 10)
    def on_start(self):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from weixin_public")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        for row in rows:
            url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query=" + row[1] + "&ie=utf8&_sug_=n&_sug_type_="
            self.crawl(url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('UL.news-list2>LI:nth-child(1)>DIV.gzh-box2>DIV.txt-box>P.tit>a').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(priority=3)
    def list_page(self, response):
        time.sleep(10)
        scriptStr = response.doc('body').text()
        if scriptStr.find("msgList", 1) != -1:
            start = scriptStr.find("msgList", 1) + 10
            end = len(scriptStr) - 42
            msg = json.loads(scriptStr[start:end])
            for each in msg["list"]:
                url = each["app_msg_ext_info"]["content_url"]
                url = url.replace("amp;", "")
                self.crawl("https://mp.weixin.qq.com" + url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        selectors = [
            ('#js_content > section > section', 'section', 'img')]
        text = ''
        for (selector1, selector2, selector3) in selectors:
            for each in response.doc(selector1).items():
                for each2 in each(selector2).items():
                    img_url = each2.attr.src
                    if img_url is not None:
                        img_url_tmp = img_url.replace('?','#')
                        img_name = img_url_tmp.replace('http://', '').replace('https://', '').replace('/', '_')
                        img_tail = '.' + img_name.split('.')[-1]
                        img_head = img_name.replace(img_tail, '').replace('.', '-')
                        img_name = img_head + img_tail
                        server_path = '/picture_hzz/' + img_name
                        local_path = os.environ['HOME'] + '/.picture_hzz/' + img_name
                        os.system('wget {} -O {}'.format(img_url, local_path))
                        part = "<p><img src={}></p>".format(server_path)  # 为了显示图片更加清楚把img标签加入p标签里面
                else:
                    part = '<p>{}</p>'.format(each.text())
                    part = part.replace('\'', '\\\'').replace('\"', '\\\"')
                text += part
            if text.replace(' ', '').replace('　', '').replace('\n', '').replace('\r', '') != '':
                break
        result = {
            "title": response.doc('#activity-name').text(),
            "time": response.doc('#post-date').text(),
            "public_signal": response.doc('#meta_content > span').text(),
            "main_body": text,
            "spider_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "url": response.url,
        }
        return result

    def on_result(self, result):
        if not result or not result['title']:
            return
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
        cur = conn.cursor()

        # 先查找是否存在
        cur.execute("select * from weixin_info where title = %s", result["title"])
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute(
                "insert into weixin_info(title,time,public_name,main_body,spider_time,url) values(%s,%s,%s,%s,%s,%s)", (
                result["title"], result["time"], result["public_signal"], result["main_body"], result["spider_time"],
                result["url"]))
        conn.commit()
        cur.close()
        conn.close()