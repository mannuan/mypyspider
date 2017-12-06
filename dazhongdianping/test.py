# -*- coding:utf-8 -*-

# 第三方模块 requests bs4 xlwt json
#
# 自带的模块urllib python2 pycharm

import requests
from bs4 import BeautifulSoup

start_url = "http://www.dianping.com/search/category/344/10/"

def get_content(url,headers=None):
    response = requests.get(url,headers=headers)#发起了一次请求
    return response.content

def region_url(html):
    soup = BeautifulSoup(html,'lxml')
    url_list = [i['href'] for i in soup.find('div',id='region-nav').find_all('a')]
    # url = soup.find('div',id='region-nav').find_all('a')
    return url_list

def get_shop_url(html):
    '''
    获取商户的详情页url地址
    :param html:
    :return:
    '''
    soup = BeautifulSoup(html, 'lxml')
    shop_list_url = soup.find_all('div',class_='tit')
    return [i.find('a')['href'] for i in shop_list_url]

def get_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('div',class_='breadcrumb').find('span').text
    price = soup.find('span',id='avgPriceTitle').text #价格
    evaluation = soup.find('span',id='comment_score').find('span',class_='item')#评分的list
    comments = soup.find('span',id='reviewCount').text #评分的数量
    address = soup.find('span',itemprop='street-address').text
    print u'店名:'+title
    for ev in evaluation:
        print ev.text
    print u'评论数量:'+comments
    print u'地址:'+address.strip()
    print u'人均价格:'+price
    return (title,evaluation[0],evaluation[1],evaluation[2],comments,address,price)

if __name__ == '__main__':
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Cookie':'_lxsdk_cuid=15fe3fc3ed0c8-026fd89dad80db-1f2a1709-1aeaa0-15fe3fc3ed0c8; _lxsdk=15fe3fc3ed0c8-026fd89dad80db-1f2a1709-1aeaa0-15fe3fc3ed0c8; _hc.v=5e7e0724-a23e-9959-4d71-7e62c30bcd1f.1511358480; __mta=55958036.1512546479523.1512546479523.1512546479523.1; JSESSIONID=93A46D38DB63CA059FBF3EE4F5F7766C; aburl=1; cy=3; cye=hangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; switchcityflashtoast=1; pvhistory="6aaW6aG1Pjo8Lz46PDE1MTI1NDcyNjM1NTRdX1s="; m_flash2=1; cityid=3; default_ab=index%3AA%3A1; source=m_browser_test_33; s_ViewType=10; _lxsdk_s=1602b5ccc5d-d5d-e57-e7e%7C%7C13','Referer':'http://www.dianping.com/shop/95087533','Host':'www.dianping.com',
    }
    base_url = 'http://www.dianping.com'
    html = get_content(start_url)
    region_url_list = region_url(html)

    for url in region_url_list:#遍历行政区
        for i in range(1,51):#遍历50页
            shop_url_list = get_shop_url(get_content(url+'p'+str(i)))
            for shop_url in shop_url_list:
                # print shop_url
                headers['Referer'] = url
                detail_html = get_content(shop_url,headers)
                print detail_html
                # items = get_detail(detail_html)
                # items = get_detail(detail_html)