# -*- coding:utf-8 -*-

import requests,json,re
from pyquery import PyQuery
from lxml import html

#加载微博参数 uid,containerid
#评论请求需要参数 id,page

# uid:5044281310
# containerid:107603 + uid

#实例方法和类方法

#正则表达式的元字符 .*?
class Tool:
    #去除img标签
    removeImg = re.compile('<img.*> | {1,7} | &nbsp;')
    #去除超链接a标签
    removeAddr = re.compile('<a.*?> | </a>')
    #把换行换成'\n'
    replaceLine = re.compile('<tr> | <div> | </div> | </p>')

    #去除所有标签
    removeTag = re.compile('<.*?>')

    @classmethod
    def replace(cls,x):
        x = re.sub(cls.removeImg,'',x)
        x = re.sub(cls.removeAddr,'',x)
        x = re.sub(cls.replaceLine,'',x)
        x = re.sub(cls.removeTag,'',x)
        return x.strip()#去掉多余的内容

class Weibo(object):

    def get_weibo(self,id,page): #个人id
        '''
        获取指定博主的所有微博
        :return: list_cards
        '''
        url = "https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}".format(id,id,id)
        reponse = requests.get(url)
        ob_json = json.loads(reponse.text)
        list_cards = ob_json.get('cards')
        return list_cards

    def get_comment(self,id,page):#微博id
        '''
        获取某条微博的所有评论
        :param id:
        :param page:
        :return:
        '''
        url = "https://m.weibo.cn/api/comments/show?id={}&page={}".format(id,page)
        response = requests.get(url)
        ob_json = json.loads(response.text)
        list_comments = ob_json.get('hot_data')
        return list_comments

    def main(self,id,page):
        list_cards = self.get_weibo(id,page)
        for card in list_cards:#遍历
            if card.get('get_type') == 9:
                id = card.get('mblog').get('id')
                text = card.get('mblog').get('text')
                text = Tool.replace(text)
                print '***'
                print u'@@@微博：'+text+'\n'

                list_comments = weibo.get_comment(id,page)
                count_hostcomments = 1
                for comment in list_comments:
                    created_at = comment.get('create_at')#获取时间
                    link_counts = comment.get('link_counts')#点赞数
                    text = comment.get('text')
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)') #用string函数过滤多余标签
                    name_user = comment.get('user').get('screen_name')
                    source = comment.get('source')
                    if source == '':
                        source = u'未知'
                    print str(count_hostcomments),':**',name_user,'**',u' **'
                    print text+'\n'
                    count_hostcomments += 1
                print '================'



if __name__ == '__main__':
    weibo = Weibo()
    # weibo.main("4174382769192599",1)
    print weibo.get_weibo('5044281310',1)