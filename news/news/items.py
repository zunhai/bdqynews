# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pripid = scrapy.Field()
    title = scrapy.Field() #新闻标题
    site = scrapy.Field() # 来源网站哪个
    url = scrapy.Field()  #新闻的url地址
    fbrq = scrapy.Field() #发布日期
    xwnr = scrapy.Field()  #新闻内容
    pass
