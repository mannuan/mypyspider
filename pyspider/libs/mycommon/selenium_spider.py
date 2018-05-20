# -*- coding:utf-8 -*-
import sys,logging,os,time,random,re,json,inspect,traceback,StringIO
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from logging.handlers import TimedRotatingFileHandler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

class SeleniumSpider(object):
    #isvirtualdisplay的优先级高于isheadless
    def __init__(self,isheadless=False,ismobile=False,isvirtualdisplay=False):
        self.isheadless = isheadless
        self.ismobile = ismobile
        self.isvirtualdisplay = isvirtualdisplay
        self.logger = self.get_logger()
        self.driver = self.get_driver()

    def __del__(self):
        self.driver.quit()

    #4 表示当前运行的层数,是通用的
    def __get_current_function_name__(self):
        return (inspect.stack()[4][3],inspect.stack()[4][2],inspect.stack()[3][3],inspect.stack()[3][2])

    def __get_running_func__(self):
        return "%s.%s[%s].%s[%s]" % (self.__class__.__name__, self.__get_current_function_name__()[0],
                               self.__get_current_function_name__()[1],
                              self.__get_current_function_name__()[2],
                              self.__get_current_function_name__()[3])

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.DEBUG)
        # handler = TimedRotatingFileHandler(filename="%s/logs/log_%s.txt"%(os.getcwd(),self.id),
        #                                    when='d',interval=1,backupCount=7)
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        # logger.addHandler(handler)
        logger.addHandler(console)
        logger.info("Start print log")
        return logger

    def get_driver(self):
        options = webdriver.ChromeOptions()
        if self.ismobile:
            options.add_argument(
                'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1"')
        else:
            options.add_argument(
            'user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36"')
        options.add_argument('lang=zh_CN.UTF-8')
        if self.isvirtualdisplay:
            self.logger.debug('virtualdisplay is running')
            display = Display(visible=0, size=(1440, 900))
            display.start()
        if self.isvirtualdisplay == False and self.isheadless == True:
            self.logger.debug('headless is running')
            options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        return driver

    def new_window(self, url):
        newwindow = 'window.open("{}");'.format(url)
        self.driver.execute_script(newwindow)

    '''
    下拉滚动加载
    times : 表示倍数
    '''
    def vertical_scroll_to(self,min_offset=1000,max_offset=5000):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight + %s)' % random.randint(min_offset,max_offset))

    def vertical_scroll_by(self,offset=100):
        self.driver.execute_script('window.scrollBy(0,%s)'%offset)

    def merge_dict(self,data1,data2):
        return dict(data1, **data2)

    def error_log(self, name='', e=None):
        if not e:
            e = ''
        fp = StringIO.StringIO()
        traceback.print_stack(file=fp)
        message = fp.getvalue()+str(e)
        self.logger.error('@%s %s: %s' % (self.__get_running_func__(),name, message))

    def warning_log(self, name='', e=None):
        if not e:
            e = ''
        self.logger.warning('@%s %s: %s' % (self.__get_running_func__(),name, e))

    def info_log(self, name='', data=None):
        if not data:
            data = ''
        self.logger.info('@%s %s: %s' % (self.__get_running_func__(),name, data))

    def debug_log(self, name='', data=None):
        if not data:
            data = ''
        self.logger.debug('@%s %s: %s' % (self.__get_running_func__(),name, data))

    def scroll_into_view(self, ele=None):
        if not ele:
            self.error_log(e='ele不可以为空')
            return None
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def focus_on_element(self, ele=None):
        if not ele:
            self.error_log(e='ele不可以为空')
            return None
        self.driver.execute_script("arguments[0].focus();", ele)

    def until_scroll_into_view_by_css_selector(self, ele=None, css_selector=None):
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return None
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def until_scroll_into_view_by_partial_link_text(self, ele=None, link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_partial_link_text(ele=ele, link_text=link_text)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def until_scroll_into_view_by_link_text(self, ele=None, link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_link_text(ele=ele,link_text=u'%s'%link_text)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def until_click_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not css_selector:
            self.error_log(e='css_selector不可以为None')
            return None
        if not ele:
            ele = self.driver
        return WebDriverWait(driver=ele, timeout=timeout)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    def until_click_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        return WebDriverWait(driver=ele, timeout=timeout)\
            .until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, u'%s'%link_text))).click()

    def until_click_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        return WebDriverWait(driver=ele, timeout=timeout)\
            .until(EC.element_to_be_clickable((By.LINK_TEXT, u'%s'%link_text))).click()

    def move_to_element(self, ele=None,xoffset=0,yoffset=0):
        if not ele:
            self.error_log(e='ele不可以为空')
            return None
        ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=xoffset,yoffset=yoffset).perform()

    def until_move_to_element_by_css_selector(self, ele=None, css_selector=None):
        if not css_selector:
            self.error_log(e='css_selector不可以为None')
            return None
        if not ele:
            ele = self.driver
        ActionChains(self.driver).move_to_element(
            self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector)).perform()

    def until_move_to_element_by_partial_link_text(self, ele=None, link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        ActionChains(self.driver).move_to_element(
            self.until_presence_of_element_located_by_partial_link_text(ele=ele,link_text=link_text)).perform()

    def until_move_to_element_by_link_text(self, ele=None, link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        ActionChains(self.driver).move_to_element(
            self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text)).perform()

    def filter_integer(self, str):
        return int(re.sub(r'[^\d]*',r'',str))

    def filter_float(self, str):
        return float(re.sub(r'[^\d.]*',r'',str))

    def filter_str(self, str):
        return re.sub(r'[\n]*',r'',str).strip()

    '''
    :param a:区间起点
    :param b:区间终点
    :param d:除数
    :return:
    '''
    def get_random_time(self, a, b, d):
        if d <= 0:
            d = 1
        c = b
        if a > b:
            b = a
        a = c
        pause_time = (lambda x: 10 if x < 10 else x)(random.random() * random.randint(a, b) / d)
        self.logger.info('...随机暂停{}秒...'.format(pause_time))
        return pause_time

    def until_send_enter_by_css_selector(self, ele=None,css_selector=None):
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector).send_keys(Keys.ENTER)

    def until_send_enter_by_link_text(self, ele=None,link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text).send_keys(Keys.ENTER)

    def until_send_enter_by_particl_link_text(self, ele=None,link_text=None):
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_partial_link_text(ele=ele,link_text=link_text).send_keys(Keys.ENTER)

    def until_send_text_by_css_selector(self, ele=None,css_selector=None, text=None):
        if not css_selector or not text:
            self.error_log(e='css_selector和text都不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector).send_keys(u'%s'%text)

    def until_get_elements_len_by_css_selector(self, ele=None, css_selector=None,timeout=1):
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return None
        if not ele:
            ele = self.driver
        return len(self.until_presence_of_all_elements_located_by_css_selector(ele=ele,css_selector=css_selector,
                                                                               timeout=timeout))

    def until_send_key_arrow_down_by_css_selector(self, ele=None,css_selector=None, min_frequency=100,max_frequency=300,
                                                  timeout=1):
        if not css_selector:
            self.error_log(e='css_selector不可以为None')
            return None
        if not ele:
            ele = self.driver
        for i in range(random.randint(min_frequency,max_frequency)):
            ActionChains(self.driver).move_to_element(
                self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout))\
                .send_keys(Keys.ARROW_DOWN).perform()

    def until_send_key_arrow_down_by_partial_link_text(self, ele=None,link_text=None, frequency=100):
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        for i in range(frequency):
            ActionChains(self.driver).move_to_element(
                self.until_presence_of_element_located_by_partial_link_text(ele=ele,link_text=link_text))\
                .send_keys(Keys.ARROW_DOWN).perform()

    def until_send_key_arrow_down_by_link_text(self, ele=None,link_text=None, frequency=100):
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        for i in range(frequency):
            ActionChains(self.driver).move_to_element(
                self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text))\
                .send_keys(Keys.ARROW_DOWN).perform()

    '''
    判断title,返回布尔值
    '''
    def until_title_is(self, ele=None, timeout=10, title=None):
        if not ele:
            ele = self.driver
        if not title:
            self.error_log(e='标题为空!!!')
            return False
        return WebDriverWait(ele, timeout).until(EC.title_is(u"%s"%title))

    '''
    判断title，返回布尔值
    '''
    def until_title_contains(self, ele=None, timeout=10, title=None):
        if not ele:
            ele = self.driver
        if not title:
            self.error_log(e='标题为空!!!')
            return False
        return WebDriverWait(ele,timeout).until(EC.title_contains(u"%s"%title))

    '''
    判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
    '''
    def until_presence_of_element_located_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.ID, id)))

    '''
    判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
    '''
    def until_presence_of_element_located_by_css_selector(self, ele=None, timeout=float(10), css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    '''
    判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
    '''
    def until_presence_of_element_located_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))

    '''
    判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
    '''
    def until_presence_of_element_located_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, link_text)))

    '''
    判断元素是否可见，如果可见就返回这个元素
    '''
    def until_visibility_of_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.ID, id)))

    '''
    判断元素是否可见，如果可见就返回这个元素
    '''
    def until_visibility_of_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.CSS_SELECTOR, css_selector)))

    '''
    判断元素是否可见，如果可见就返回这个元素
    '''
    def until_visibility_of_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.LINK_TEXT, link_text)))

    '''
    判断元素是否可见，如果可见就返回这个元素
    '''
    def until_visibility_of_by_particl_link_text(self, ele=None, timeout=10, partial_link_text=None):
        if not ele:
            ele = self.driver
        if not partial_link_text:
            self.error_log(e='partial_link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.PARTIAL_LINK_TEXT, partial_link_text)))

    '''
    判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
    '''
    def until_presence_of_all_elements_located_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.ID, id)))

    '''
    判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
    '''
    def until_presence_of_all_elements_located_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    '''
    判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
    '''
    def until_presence_of_all_elements_located_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.LINK_TEXT, link_text)))

    '''
    判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
    '''
    def until_presence_of_all_elements_located_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, u'%s'%link_text)))

    '''
    判断是否至少有一个元素在页面中可见，如果定位到就返回列表
    '''
    def until_visibility_of_any_elements_located_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.ID, id)))

    '''
    判断是否至少有一个元素在页面中可见，如果定位到就返回列表
    '''
    def until_visibility_of_any_elements_located_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    '''
    判断是否至少有一个元素在页面中可见，如果定位到就返回列表
    '''
    def until_visibility_of_any_elements_located_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.LINK_TEXT, link_text)))

    '''
    判断是否至少有一个元素在页面中可见，如果定位到就返回列表
    '''
    def until_visibility_of_any_elements_located_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, link_text)))

    '''
    判断指定的元素中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_located_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.ID, id)))

    '''
    判断指定的元素中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_located_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    '''
    判断指定的元素中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_located_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.LINK_TEXT, link_text)))

    '''
    判断指定的元素中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_located_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, link_text)))

    '''
    判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_value_by_id(self, ele=None, timeout=10, id=None, _text=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.ID, id),u'%s'%_text))

    '''
    判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_value_by_css_selector(self, ele=None, timeout=10, css_selector=None, _text=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, css_selector),
                                                                                        u'%s'%_text))

    '''
    判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_value_by_link_text(self, ele=None, timeout=10, link_text=None, _text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.LINK_TEXT, link_text),
                                                                                        u'%s'%_text))

    '''
    判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
    '''
    def until_text_to_be_present_in_element_value_by_partial_link_text(self, ele=None, timeout=10, link_text=None, _text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.PARTIAL_LINK_TEXT, link_text),
                                                                                        u'%s' % _text))

    '''
    判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False
    '''
    def until_frame_to_be_available_and_switch_to_it(self, ele=None, timeout=10):
        if not ele:
            ele = self.driver
        return WebDriverWait(ele, timeout).until(EC.frame_to_be_available_and_switch_to_it(ele))

    '''
    判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
    '''
    def until_invisibility_of_element_located_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.ID, id)))

    '''
    判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
    '''
    def until_invisibility_of_element_located_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector)))

    '''
    判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
    '''
    def until_invisibility_of_element_located_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.LINK_TEXT, link_text)))

    '''
    判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
    '''
    def until_invisibility_of_element_located_by_partial_link_text(self, ele=None, timeout=10, partial_link_text=None):
        if not ele:
            ele = self.driver
        if not partial_link_text:
            self.error_log(e='partial_link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.LINK_TEXT, partial_link_text)))

    '''
    判断某个元素中是否可见并且是enable的，代表可点击
    '''
    def until_element_to_be_clickable_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.ID, id)))

    '''
    判断某个元素中是否可见并且是enable的，代表可点击
    '''
    def until_element_to_be_clickable_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

    '''
    判断某个元素中是否可见并且是enable的，代表可点击
    '''
    def until_element_to_be_clickable_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))

    '''
    判断某个元素中是否可见并且是enable的，代表可点击
    '''
    def until_element_to_be_clickable_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text)))

    '''
    等待某个元素从dom树中移除
    '''
    def until_staleness_of_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.ID, id)))

    '''
    等待某个元素从dom树中移除
    '''
    def until_staleness_of_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.CSS_SELECTOR, css_selector)))

    '''
    等待某个元素从dom树中移除
    '''
    def until_staleness_of_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.LINK_TEXT, link_text)))

    '''
    等待某个元素从dom树中移除
    '''
    def until_staleness_of_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.PARTIAL_LINK_TEXT, link_text)))

    '''
    判断某个元素是否被选中了,一般用在下拉列表
    '''
    def until_element_to_be_selected_by_id(self, ele=None, timeout=10, id=None):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.ID, id)))

    '''
    判断某个元素是否被选中了,一般用在下拉列表
    '''
    def until_element_to_be_selected_by_css_selector(self, ele=None, timeout=10, css_selector=None):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.CSS_SELECTOR, css_selector)))

    '''
    判断某个元素是否被选中了,一般用在下拉列表
    '''
    def until_element_to_be_selected_by_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.LINK_TEXT, link_text)))

    '''
    判断某个元素是否被选中了,一般用在下拉列表
    '''
    def until_element_to_be_selected_by_partial_link_text(self, ele=None, timeout=10, link_text=None):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.PARTIAL_LINK_TEXT, link_text)))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_selection_state_to_be_by_id(self, ele=None, timeout=10, id=None, status=True):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.ID, id),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_selection_state_to_be_by_css_selector(self, ele=None, timeout=10, css_selector=None, status=True):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.CSS_SELECTOR, css_selector),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_selection_state_to_be_by_link_text(self, ele=None, timeout=10, link_text=None, status=True):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.LINK_TEXT, link_text),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_selection_state_to_be_by_partial_link_text(self, ele=None, timeout=10, link_text=None, status=True):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.PARTIAL_LINK_TEXT, link_text),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_located_selection_state_to_be_by_id(self, ele=None, timeout=10, id=None, status=True):
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.ID, id),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_located_selection_state_to_be_by_css_selector(self, ele=None, timeout=10, css_selector=None, status=True):
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, css_selector),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_located_selection_state_to_be_by_link_text(self, ele=None, timeout=10, link_text=None, status=True):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.LINK_TEXT, link_text),status))

    '''
    判断某个元素的选中状态是否符合预期
    '''
    def until_element_located_selection_state_to_be_by_partial_link_text(self, ele=None, timeout=10, link_text=None, status=True):
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.PARTIAL_LINK_TEXT, link_text),
                                                                                          status))

    '''
    判断页面上是否存在alert,如果有就切换到alert并返回alert的句柄
    '''
    def until_alert_is_present(self, ele=None, timeout=10):
        if not ele:
            ele = self.driver
        return WebDriverWait(ele, timeout).until(EC.alert_is_present())

    '''
    获得店铺的关键字段
    field : 字段的名字
    ele : webelement
    css_selector : str
    attr : str
    regex : str 正则表达式用来去掉不需要的
    '''
    def get_key_str_field_by_css_selector(self, name='new', ele=None, css_selector=None, attr=None, regex='', repl='', timeout=1,
                                          offset=20,try_times=20):
        regex = u'%s'%regex
        repl = u'%s'%repl
        try:
            if ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout)
            elif ele and not css_selector:
                ele = ele
            elif not ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=css_selector,timeout=timeout)
            else:
                self.error_log(name=name,e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if attr:
                _str = ele.get_attribute(attr)
            else:
                _str = ele.text
            _str = self.filter_str(_str)
            _str = re.sub('%s' % regex, '%s' % repl, _str)
        except Exception as e:
            self.error_log(name=name, e=e)
            _str = None
        self.info_log(name=name, data=_str)
        return _str

    def get_str_field_by_css_selector(self, name='new', ele=None, css_selector=None, attr=None, regex='',repl='', timeout=1,
                                      offset=100,try_times=20):
        regex = u'%s'%regex
        repl = u'%s'%repl
        try:
            if ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout)
            elif ele and not css_selector:
                ele = ele
            elif not ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=css_selector,timeout=timeout)
            else:
                self.error_log(name=name, e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if attr:
                _str = ele.get_attribute(attr)
            else:
                _str = ele.text
            _str = self.filter_str(_str)
            _str = re.sub('%s' % regex, '%s' % repl, _str)
        except Exception as e:
            self.error_log(name=name, e=e)
            _str = None
        self.info_log(name=name, data=_str)
        return _str

    def get_str_list_field_by_css_selector(self, name='new', ele=None, list_css_selector=None,
                                     item_css_selector=None, attr=None, regex='', repl='',timeout=1):
        regex = u'%s'%regex
        repl = u'%s'%repl
        _list = []
        try:
            list_ele = self.until_presence_of_element_located_by_css_selector(
                ele=ele,css_selector=list_css_selector,timeout=timeout)
            if not list_ele:
                self.warning_log(name=name,e='该字段为空')
                return None
            for item in self.until_presence_of_all_elements_located_by_css_selector(
                    ele=list_ele,css_selector=item_css_selector,timeout=timeout):
                _str = self.get_str_field_by_css_selector(name=name,ele=item,attr=attr,regex=regex,repl=repl,timeout=timeout)
                if _str:
                    _list.append(_str)
        except Exception as e:
            self.error_log(name=name,e=e)
        self.info_log(name=name, data=_list)
        return _list

    def get_int_field_by_css_selector(self, name='new', ele=None, css_selector=None, attr=None, regex='',repl='', timeout=1,
                                      offset=20,try_times=20):
        regex = u'%s'%regex
        repl = u'%s'%repl
        try:
            if ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout)
            elif ele and not css_selector:
                ele = ele
            elif not ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=css_selector,timeout=timeout)
            else:
                self.error_log(name=name, e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if attr:
                _str = ele.get_attribute(attr)
            else:
                _str = ele.text
            _str = self.filter_str(_str)
            _str = re.sub('%s' % regex, '%s' % repl, _str)
            _int = self.filter_integer(_str)
        except Exception as e:
            self.error_log(name=name, e=e)
            _int = 0
        self.info_log(name=name, data=str(_int))
        return _int

    def get_float_field_by_css_selector(self,name='new', ele=None, css_selector=None, attr=None, regex='',repl='', timeout=1,
                                        offset=20,try_times=20):
        regex = u'%s'%regex
        repl = u'%s'%repl
        try:
            if ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector, timeout=timeout)
            elif ele and not css_selector:
                ele = ele
            elif not ele and css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=css_selector,offset=offset,timeout=timeout,try_times=try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=css_selector, timeout=timeout)
            else:
                self.error_log(name=name, e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if attr:
                _str = ele.get_attribute(attr)
            else:
                _str = ele.text
            _str = self.filter_str(_str)
            _str = re.sub('%s' % regex, '%s' % repl, _str)
            _float = self.filter_float(_str)
        except Exception as e:
            self.error_log(name=name, e=e)
            _float = 0.0
        self.info_log(name=name, data=str(_float))
        return _float

    '''
    运行一个新建标签页的任务(默认根据url打开标签页)
    '''
    def run_new_tab_task(self, click_css_selector=None, name='', func=None, url=None,pause_time=1, **args):
        if not func:
            self.warning_log(name=name, e='标签页任务里面没有具体要执行的内容!!!')
            return None
        if not url:
            self.error_log(name=name,e='标签页任务里面没有具体要打开的url!!!')
            return None
        self.new_window(url)
        self.driver.switch_to_window(self.driver.window_handles[-1])
        time.sleep(pause_time)
        data = func(**args)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return data

    '''
    运行一个新标签页的任务(通过按钮点击打开标签页)
    '''
    def run_tab_task(self, click_ele=None, name='', func=None,pause_time=1,offset=8,try_times=20, **args):
        if not func:
            self.warning_log(name=name, e='标签页任务里面没有具体要执行的内容!!!')
            return None
        if not click_ele:
            self.error_log(name=name,e='click_ele不可以为空')
            return None
        self.until_click_by_vertical_scroll_page_down(click_ele=click_ele,offset=offset,try_times=try_times)
        self.driver.switch_to_window(self.driver.window_handles[-1])
        time.sleep(pause_time)
        data = func(**args)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return data

    def run_spider(self):
        pass

    '''
    通过长度判断页面是否有更多
    '''
    def ismore_by_scroll_page_judge_by_len(self, css_selector,min_offset=1000,max_offset=5000,comment_len=None):
        self.info_log(data='...开始下拉页面...')
        while (True):
            list_len = self.until_get_elements_len_by_css_selector(
                css_selector=css_selector,timeout=1)
            self.vertical_scroll_to(min_offset=min_offset,max_offset=max_offset)
            list_len2 = self.until_get_elements_len_by_css_selector(css_selector=css_selector,timeout=1)
            self.info_log(data='当前数量%s:' % list_len2)
            if list_len == list_len2:
                if comment_len:
                    if list_len2 >= comment_len:
                        break
                time.sleep(2)
                self.vertical_scroll_to(min_offset=min_offset,max_offset=max_offset)
                list_len2 = self.until_get_elements_len_by_css_selector(css_selector=css_selector,timeout=1)
                if list_len == list_len2:
                    break
        self.logger.info('...结束下拉页面...')

    '''
    通过长度判断页面是否有更多
    list_css_selector : 列表的css样式
    ele_css_selector : 发送向下指令的元素的css样式
    frequency : 表示按向下键的次数
    '''
    def until_ismore_by_send_key_arrow_down_judge_by_len(self, list_css_selector=None,ele_css_selector=None,
        min_frequency=100,max_frequency=300,comment_len=None,timeout=1):
        if not list_css_selector:
            self.error_log(e='list_css_selector不可以为空!!!')
            return None
        if not ele_css_selector:
            self.error_log(e='ele_css_selector不可以为空!!!')
            return None
        self.info_log(data='...开始下拉页面...')
        while (True):
            list_len = self.until_get_elements_len_by_css_selector(css_selector=list_css_selector,timeout=timeout)
            self.until_send_key_arrow_down_by_css_selector(css_selector=ele_css_selector,
                             min_frequency=min_frequency,max_frequency=max_frequency,timeout=timeout)
            list_len2 = self.until_get_elements_len_by_css_selector(css_selector=list_css_selector)
            self.info_log(data='当前数量%s:' % list_len2)
            if list_len == list_len2:
                if comment_len:
                    if list_len2 >= comment_len:
                        break
                time.sleep(2)
                self.until_send_key_arrow_down_by_css_selector(css_selector=ele_css_selector,
                                  min_frequency=min_frequency,max_frequency=max_frequency,timeout=timeout)
                list_len2 = self.until_get_elements_len_by_css_selector(css_selector=list_css_selector,timeout=timeout)
                if list_len == list_len2:
                    break
        self.logger.info('...结束下拉页面...')

    def until_click_by_vertical_scroll_page_down(self,click_ele=None,offset=8,try_times=20):
        failed_times = 0
        while(True):
            self.scroll_into_view(ele=click_ele)
            if failed_times > try_times:
                break
            try:
                click_ele.click()
                self.info_log(data='点击成功')
                break
            except Exception:
                failed_times += 1
                self.warning_log(e='...正在尝试第%s次点击...'%failed_times)
                self.vertical_scroll_by(offset=offset)

    def until_presence_by_vertical_scroll_page_down_by_css_selector(self,ele=None,css_selector=None,offset=8,try_times=20,timeout=1):
        if not css_selector:
            self.error_log(e='css_selector不允许为空!!!')
            return None
        if not ele:
            ele = self.driver
        failed_times = 0
        while(True):
            if failed_times > try_times:
                break
            try:
                self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=float(timeout)/10)
                self.info_log(data='元素存在,可以访问')
                break
            except Exception:
                failed_times += 1
                self.warning_log(e='...正在尝试第%s次下拉...'%failed_times)
                self.vertical_scroll_by(offset=offset)

    def until_refresh_by_css_selector(self,css_selector,try_times=10):
        count = 0
        if not css_selector:
            self.error_log(e='css_selector不可以为空!!!')
            return None
        for i in range(try_times):
            try:
                self.until_presence_of_element_located_by_css_selector(css_selector=css_selector,timeout=1)
            except Exception as e:
                count += 1
                self.info_log(data='第%s次刷新!!!'%count)
                self.driver.refresh()

    '''
    根据css样式点击直到没有下一页
    '''
    def until_click_no_next_page_by_css_selector(self,func=None,css_selector=None,timeout=1,pause_time=1,**kwargs):
        if not css_selector:
            self.error_log(e='css_selector不可以为空!!!')
            return None
        count = 0
        self.vertical_scroll_to(min_offset=0, max_offset=0)
        while(True):
            self.until_scroll_into_view_by_css_selector(css_selector=css_selector)
            func(**kwargs)
            time.sleep(pause_time)
            try:
                self.until_click_by_css_selector(css_selector=css_selector,timeout=timeout)
                count += 1
                self.info_log(data='点击第%s页...'%count)
            except Exception as e:
                self.error_log(e='没有下一页了!!!')
                break

    '''
    根据链接文字点击直到没有下一页
    '''
    def until_click_no_next_page_by_link_text(self,func=None,link_text=None,timeout=1,pause_time=1,**kwargs):
        if not link_text:
            self.error_log(e='link_text不可以为空!!!')
            return None
        count = 0
        self.vertical_scroll_to(min_offset=0, max_offset=0)
        while(True):
            self.until_scroll_into_view_by_link_text(link_text=link_text)
            func(**kwargs)
            time.sleep(pause_time)
            try:
                self.until_click_by_link_text(link_text=link_text,timeout=timeout)
                count += 1
                self.info_log(data='点击第%s页...'%count)
            except Exception as e:
                self.error_log(e='没有下一页了!!!')
                break

    '''
    根据部分链接文字点击直到没有下一页
    '''
    def until_click_no_next_page_by_partical_link_text(self,func=None,link_text=None,timeout=1,pause_time=1,**kwargs):
        if not link_text:
            self.error_log(e='link_text不可以为空!!!')
            return None
        count = 0
        self.vertical_scroll_to(min_offset=0,max_offset=0)
        while(True):
            self.until_scroll_into_view_by_partial_link_text(link_text=link_text)
            func(**kwargs)
            time.sleep(pause_time)
            try:
                self.until_click_by_partial_link_text(link_text=link_text,timeout=timeout)
                count += 1
                self.info_log(data='点击第%s页...'%count)
            except Exception as e:
                self.error_log(e='没有下一页了!!!')
                break

    '''
    关闭先前的页面
    '''
    def close_pre_page(self):
        self.driver.switch_to_window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    '''
    根据索引切换浏览器窗口
    '''
    def switch_window_by_index(self,index=None):
        if not index:
            self.error_log(e='index不可以为空!!!')
            return None
        self.driver.switch_to_window(self.driver.window_handles[index])

    def isneed_to_update_comment_data(self):
        pass