# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from scrapy.cmdline import execute

execute(['scrapy', 'crawl', 'duanzi'])