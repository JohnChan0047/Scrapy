# -*- coding:utf-8 -*- 
__author__ = 'John 2017/12/30 16:32'
from scrapy.cmdline import execute

import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'zhihu'])