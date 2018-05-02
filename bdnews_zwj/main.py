from scrapy.cmdline import execute
import os
import sys
#coding=utf-8
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","bdnews2"])
