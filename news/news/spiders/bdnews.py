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



class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['http://www.baidu.com/']

    conn = pymysql.connect(host='192.168.3.232', user='zwj', passwd='123456', db='caiji', charset='utf8',
                           port=3306)
    cursor = conn.cursor()


    def start_requests(self):
         for i in range(0, 1000):
            sql = 'select ID,PRIPID,ENTNAME from HLJ_E_BASEINFO where ID>=%s and ID<%s'%(150000+i*100, 150000+(i+1)*100)
            print(sql)
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
            headers = {'User-Agent': user_agent}            
            if rs:
                for bs in rs:
                    kw = bs[2]
                    pripid = bs[1]
                    id = bs[0]
                    try:
                        time.sleep(0.1)
                        url = 'http://news.baidu.com/ns?word={0}&tn=news&from=news&cl=2&rn=20&ct=1'.format(kw)
                        # url = 'http://news.baidu.com/ns?ct=1&rn=30&ie=utf-8&bs=%E9%BB%91%E9%BE%99%E6%B1%9F%E5%86%9C%E5%9E%A6%E5%BB%BA%E8%AE%BE%E5%B7%A5%E7%A8%8B%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E9%BB%91%E9%BE%99%E6%B1%9F%E5%86%9C%E5%9E%A6%E5%BB%BA%E8%AE%BE%E5%B7%A5%E7%A8%8B%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83'
                        yield scrapy.Request(url, headers=headers, meta={"pripid": pripid}, callback=self.parse2)
                    except Exception, e:
                        print(e)
                        # print(id)

    def parse2(self, response):
        try:
            hx = Selector(response)
            
            pirpid = response.meta["pripid"]
            # print(pirpid)
            # url = response.meta["url"]
            item = NewsItem()
            item['pripid'] = pirpid  
            # print(item['pripid'])          
            div = hx.xpath('//div[@class="result"]')
            for i in range(0, len(div)):
                micro = div[i]
                infourl = micro.xpath('./div/span/a[@class="c-more_link"]/@href').extract()
                new_url = ''.join(infourl)
                # print(new_url)
                if new_url:                   
                    new_url = 'http://news.baidu.com'+new_url        
                    # print(new_url)
                    item['url'] = new_url
                    yield item
                    # yield scrapy.Request(url=new_url , meta = {"pirpid" : pirpid} ,callback=self.parse3)
                else:
                    new_url=""
                yield item   
                # yield scrapy.Request(url=new_url , meta = {"pirpid" : pirpid} ,callback=self.parse3)

        except Exception, e:
            print(e)




    # def parse3(self, response):
    #     try:
    #         hx = Selector(response)
    #         div = hx.xpath('//div[@class="result"]')
    #         pid = response.meta["pripid"]
    #         print(pid)
    #         for i in range(0, len(div)):
    #             micro = div[i]
    #             t_url = micro.xpath("./h3/a/@href").extract_first()
    #             url = ''.join(t_url)

    #             rs = None
    #             # sql_s = 'select 1 from HLJ_QYNEWS where url="%s"'%url
    #             # self.cursor.execute(sql_s)
    #             # rs = self.cursor.fetchall()
    #             if rs:
    #                 pass
    #             else:
    #                 item = NewsItem()
    #                 item['pripid'] = pid
    #                 item['url'] = url

    #                 t_title = micro.xpath('./h3/a')
    #                 tm_title = t_title.xpath("string(.)").extract()
    #                 title = ''.join(tm_title)
    #                 item['title'] = title

    #                 aut = micro.xpath('.//p[@class="c-author"]/text()').extract()
    #                 author = ''.join(aut)
    #                 reg = r'\d{4}'
    #                 ssnum = re.search(reg, author)

    #                 if ssnum:
    #                     ssnum = ssnum.span()
    #                     site = author[0:ssnum[0]]
    #                     fbrq = author[ssnum[0]:]
    #                     item['site'] = site

    #                     item['fbrq'] = fbrq
    #                 else:
    #                     item['site'] = ''
    #                     item['fbrq'] = ''

    #                 summary = micro.xpath('./div[@class="c-summary c-row "]')

    #                 if summary:
    #                     xwnr = ''.join(summary.extract()).split('</p>')[1].split('<span')[0].replace('<em>', '').replace('</em>', '')

    #                     item['xwnr'] = xwnr
    #                 else:
    #                     item['xwnr'] = ''
    #                 yield item
    #     except Exception, e:
    #         print(e)