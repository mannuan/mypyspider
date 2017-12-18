# -*- coding:utf-8 -*-

from pyspider.libs.base_handler import *
import json,pymysql


class Handler(BaseHandler):
    crawl_config = {
        'headers': {'Content-Type': 'application/json; charset=utf-8'}
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for page in range(1,22):
            url = 'http://m.elong.com/hotel/api/list?city=1233&pageindex={}'.format(page)
            self.crawl(url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        result = []
        ob_json = response.json
        list_shops = ob_json.get('hotelList')
        if list_shops is None:
            return None
        for shop in list_shops:  # 遍历
            activityTags = json.dumps(shop.get('activityTags'))
            baiduLatitude = shop.get('baiduLatitude')
            baiduLongitude = shop.get('baiduLongitude')
            businessAreaName = shop.get('businessAreaName')
            calDistanceType = shop.get('calDistanceType')  # int
            commentPoint = shop.get('commentPoint')
            commentScore = shop.get('commentScore')  # int
            id = str(shop.get('detailPageUrl')).split('hotel/')[1].split('/#indate')[0]
            distance = shop.get('distance')
            distanceName = shop.get('distanceName')
            districtName = shop.get('districtName')
            facilityList = json.dumps(shop.get('facilityList'))
            hongbao = shop.get('hongbao')  # int
            hotelBadge = shop.get('hotelBadge')  # int
            hotelName = shop.get('hotelName')
            leftRoomCountShow = shop.get('leftRoomCountShow')
            lmOriPrice = shop.get('lmOriPrice')  # int
            lowestPrice = shop.get('lowestPrice')  # int
            minPriceInventories = shop.get('minPriceInventories')
            minPriceSubCouponInventories = json.dumps(shop.get('minPriceSubCouponInventories'))
            newRecallReason = shop.get('newRecallReason')
            picUrl = shop.get('picUrl')
            placeName = shop.get('placeName')
            specialDay = shop.get('specialDay')
            starLevel = shop.get('starLevel')  # int
            syncfacilityList = shop.get('syncfacilityList')
            tags = json.dumps(shop.get('tags'))
            totalCommentCount = shop.get('totalCommentCount')#int
            trafficInfo = shop.get('trafficInfo')
            result.append([activityTags,baiduLatitude,baiduLongitude,businessAreaName,calDistanceType,commentPoint,commentScore,id,distance,distanceName,districtName,facilityList,hongbao,hotelBadge,hotelName,leftRoomCountShow,lmOriPrice,lowestPrice,minPriceInventories,minPriceSubCouponInventories,newRecallReason,picUrl,placeName,specialDay,starLevel,syncfacilityList,tags,totalCommentCount,trafficInfo])
        return result

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    def on_result(self, result):
        if not result:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8mb4')
        cur = conn.cursor()
        try:
            sql = 'REPLACE INTO elong_shop values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            # 批量插入
            cur.execute(sql,result)
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
        # 释放数据连接
        if cur:
            cur.close()
        if conn:
            conn.close()