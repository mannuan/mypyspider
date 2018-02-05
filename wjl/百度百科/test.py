# -*- coding:utf-8 -*-
import urlparse,os,re,pymysql,time
from pyquery import PyQuery

def filter_page(pq, *args):
    server_path = '/picture_hzz/'
    local_path = os.environ['HOME'] + '/.picture_hzz/'
    content = ''
    for cs in args:
        p = pq(cs)  # rd是一个PyQuery对象
        p('script').remove()#去除script标签
        p('style').remove()#去除style标签
        content += (
        lambda x: '' if x is None else re.sub(r'[ ]+[^ \"</>=]+[ ]*=[ ]*?\"(?!https://|http://)[^\"<>]*?\"|[\f\n\r]+', '',x))(p.html())#先去除没有用的class和style属性
    original_url_list = []
    regex = re.compile(r'<(?!div|img)[^ </>\"]+([^<>]*)[ ]+(?!href)[^ </>\"]+[ ]*=[ ]*?\"((?=https://|http://)[^ \"<>]+)?\"([^<>]*)[/]{0,1}?>')#标签不是img
    content = regex.sub(r'<img\1 src="\2"\3>', content)#更改为img标签
    original_url_list.extend([url[1] for url in regex.findall(content)])#原始的img url
    regex = re.compile(r'<(?=img)[^ </>\"]+([^<>]*)[ ]+(?=src)[^ </>\"]+[ ]*=[ ]*?\"((?=https://|http://)[^ \"<>]+)?\"([^<>]*)[/]{0,1}?>')#标签是img
    content = regex.sub(r'<img\1 src="\2"\3>', content)  # 更改为img标签
    original_url_list.extend([url[1] for url in regex.findall(content)])#原始的img url
    url_list = []#可用于下载的img url
    for i in range(len(original_url_list)):#过滤img url
        params = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(original_url_list[i]).query).items()])
        if len(params) != 0:
            url = (lambda url, src: url.split('?')[0] if src is None else src)(original_url_list[i],params.get('src'))#修改后的img url
            url_list.append(url)
            content = content.replace(original_url_list[i],url)
        else:
            url_list.append(original_url_list[i])
    time_list = []
    for i in range(len(original_url_list)):
        name = str(time.time()).replace('.', '')
        time_list.append(name)
        time.sleep(0.01)
    pic_list = []
    download_pic_list = []
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository',charset='utf8')
    cur = conn.cursor()
    for i in range(len(original_url_list)):
        cur.execute("select name,url from hzz_local_picture where url = %s", url_list[i])
        row = cur.fetchone()
        if row is None:
            cur.execute("insert into hzz_local_picture values(%s,%s)", [time_list[i], url_list[i]])
            pic_list.append((time_list[i], url_list[i]))
            download_pic_list.append((time_list[i], url_list[i]))
        else:
            pic_list.append((row[0].encode('utf-8'), row[1].encode('utf-8')))
        conn.commit()
    cur.close()
    conn.close()
    for pic in pic_list:
        content = content.replace(pic[1], server_path + pic[0])
    for pic in download_pic_list:
        os.system('wget {} -O {}'.format(pic[1], local_path + pic[0]))
    return content

with open('/home/mininet/test1.html','r') as f:
    content = f.read().strip()
    f.close()
content = filter_page(PyQuery(content),
                     '#J-lemma > div.BK-body-wrapper > div.BK-before-content-wrapper',
                     '#J-lemma > div.BK-body-wrapper > div.BK-content-wrapper')
# content = filter_page(PyQuery(content),'body > div.body-wrapper > div.content-wrapper')
#p = PyQuery(content)
# p('#J-lemma > div.header-wrapper')
# content = p.html()
print content