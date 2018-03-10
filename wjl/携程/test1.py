# -*- coding:utf-8 -*-

import requests,json
payload = {"adultCounts":0,"checkinDate":"20180308","checkoutDate":"20180309","cityID":1332,"cityName":"千岛湖","controlBitMap":1,"costPerformanceHigh":False,"districtID":0,"domesticHotelList":"domesticHotelList","filterItemList":[],"highestPrice":0,"hotelIdList":[],"keyword":"","locationItemList":["distance-4|||4公里以内|@distance"],"lowestPrice":0,"orderItem":"sort-4|2","oversea":False,"overseaHotelList":"overseaHotelList","pageIndex":2,"pageSize":10,"roomQuantity":0,"searchByExposedHotSearchKeyword":False,"searchByExposedZone":False,"showCheckinDate":"03-08","showCheckoutDate":"03-09","starItemList":[],"userLatitude":29.6045894622803,"userLocationSearch":True,"userLongitude":119.034812927246,"validCheckinDate":"20180308"}
payload = json.dumps(payload)

r = requests.post("http://m.ctrip.com/webapp/hotel/j/hotellistbody?pageid=212093&key=67f59cc7cf43026622df373827e4713185309d242ef1099d3bbedfae7e53cccd", data=payload)
print(r.text)