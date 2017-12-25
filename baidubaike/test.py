# -*- coding:utf-8 -*-
import urllib
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


def cbk(a, b, c):
    '''回调函数 
    @a: 已经下载的数据块 
    @b: 数据块的大小 
    @c: 远程文件的大小 
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per


# urllib.urlretrieve(url, local, cbk)
url = 'https://wapbaike.baidu.com/item/盂溪'
local = '/home/quick_picture/盂溪_baidubaike.html'
urllib.urlretrieve(url, local)
