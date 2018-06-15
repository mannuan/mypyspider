# -*- encoding:utf-8 -*-

class Regex(object):
    HTML_IMG_SRC_REGEX = r'<(?=img)[^ </>\"]+[^<>]*[ ]+(?=src|data-src)[^ </>\"]+[ ]*=[ ]*?\"((?=https://|http://)[^ \"<>]+)?\"[^<>]*[/]{0,1}?>'