#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-25 15:24:21
# Project: test8

from pyspider.libs.base_handler import *
import lxml


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.tba.gov.cn//tba/content/TBA/xwzx/jczt/hcz/gzdt/0000000000012456.html', fetch_type='js',
                   callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for c in response.doc('#print > tbody > tr:nth-child(5) > td > table > tbody > tr > td').items('p'):
            print c.html()

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }