# -*- encoding:utf-8 -*-
import pymysql
import json
import os

'''
合并字典类型数据
'''
def merge_dict(data1, data2):
    return dict(data1, **data2)

'''
取得一个数据库链接
'''
def get_db_conn(host='localhost',port=3306,user='repository',passwd='repository',db='repository',charset='utf8'):
    return pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,charset=charset)

'''
@:param key :更新的关键字
@:param data :要插入的数据,数据类型是字典
@:return 无返回值
'''
def save_data(host='localhost',port=3306,user='repository',passwd='repository',db='repository',charset='utf8',table='',key='',data={}):
    if not table or not key or not data:#如果数据为空
        return
    conn = get_db_conn(host=host,port=port,user=user,passwd=passwd,db=db,charset=charset)
    cur = conn.cursor()
    cur.execute("select * from %s where %s = \'%s\'"%(table, key, data[key]))
    rows = cur.fetchall()
    if len(rows) == 0:
        try:
            sql = "INSERT INTO %s(%s) values(%s)"%(table,(lambda d: ",".join(d.keys()))(data),','.join(['%s']*len(data)))
            cur.execute(sql,data.values())
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
    else:
        try:
            sql = "UPDATE %s SET %s WHERE url=\'%s\'"%(table,(lambda d: "=%s,".join(list(filter(lambda d: False if d == key else True, data.keys()))))(data)+'=%s',data[key])
            cur.execute(sql,list(data.get(k) for k in filter(lambda d:False if d == key else True, data.keys())))
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
    # 释放数据连接
    if cur:
        cur.close()
    if conn:
        conn.close()

'''
@return 返回值是一个列表
'''
def query_data(host='localhost',port=3306,user='repository',passwd='repository',db='repository',charset='utf8',table='',key='',key_value='',field=''):
    if not table:
        print 'table不可以为空!!!'
        return
    if not field:
        field = '*'
    conn = get_db_conn(host=host,port=port,user=user,passwd=passwd,db=db,charset=charset)
    cur = conn.cursor()
    if not key:
        cur.execute("select %s from %s"%(field,table))
    else:
        if not key_value:
            print 'key_value不可以为空!!!'
            return
        else:
            cur.execute("select %s from %s where %s = %s" % (field, table,key,key_value))
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows

'''
下载图片
'''
def download_img(url,path):
    os.system('wget %s -O %s' % (url, path))


if __name__ == '__main__':
    # save_data(table='weixin_info', key='url',data={'title': 'www.你妈.com', 'time': 'www.2020年.com', 'public_name': 'www.御姐.com', 'main_body': 'www.卡上就付款链接打开了.com', 'spider_time': 'www.2030年.com','url': 'www.fuck.com'})
    print query_data(table='weixin_public',field='public_name')