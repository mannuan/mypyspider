# -*- coding: utf8 -*-
import re

html = """ 
  <div class="w-number"> <span class="tpte">14℃</span> </div> 
"""

if __name__ == '__main__':
    p = re.compile('<[^>]+>')
    print p.sub("", html)