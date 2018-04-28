#!/usr/bin/python
# -*- coding:utf-8 -*-
import scrapy
import re
import pymysql
from scrapy.selector import Selector
from news.items import NewsItem
# from scrapy.http import Request
import sys
import os
import time
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
class HycSpider(scrapy.Spider):
    name = 'down'
    allowed_domains = ['news.baidu.com']
    start_urls = [
        'http://news.baidu.com',
    ]

    def start_requests(self):
        url = ''
        with open('xxx.json' , encoding='utf-8') as f:
            for i in range(100000):
                url = f.readline().strip('\n')
                try:
                    yield scrapy.Request(url=url , meta = {"url" : url} ,callback=self.parse2)
                except:
                    pass
    def parse2(self, response):
        try:
            hx = Selector(response)
            div = hx.xpath('//div[@class="result"]')
            pid = response.meta["pripid"]
            print(pid)
            for i in range(0, len(div)):
                micro = div[i]
                t_url = micro.xpath("./h3/a/@href").extract_first()
                url = ''.join(t_url)

                rs = None
                # sql_s = 'select 1 from HLJ_QYNEWS where url="%s"'%url
                # self.cursor.execute(sql_s)
                # rs = self.cursor.fetchall()
                if rs:
                    pass
                else:
                    item = NewsItem()
                    item['pripid'] = pid
                    item['url'] = url

                    t_title = micro.xpath('./h3/a')
                    tm_title = t_title.xpath("string(.)").extract()
                    title = ''.join(tm_title)
                    item['title'] = title

                    aut = micro.xpath('.//p[@class="c-author"]/text()').extract()
                    author = ''.join(aut)
                    reg = r'\d{4}'
                    ssnum = re.search(reg, author)

                    if ssnum:
                        ssnum = ssnum.span()
                        site = author[0:ssnum[0]]
                        fbrq = author[ssnum[0]:]
                        item['site'] = site

                        item['fbrq'] = fbrq
                    else:
                        item['site'] = ''
                        item['fbrq'] = ''

                    summary = micro.xpath('./div[@class="c-summary c-row "]')

                    if summary:
                        xwnr = ''.join(summary.extract()).split('</p>')[1].split('<span')[0].replace('<em>', '').replace('</em>', '')

                        item['xwnr'] = xwnr
                    else:
                        item['xwnr'] = ''
                    yield item
        except Exception, e:
            print(e)