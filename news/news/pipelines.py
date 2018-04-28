# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json

#保证可以向oracle数据库中更新中文
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class NewsPipeline(object):
    def process_item(self, item, spider):
#         #连接数据库
#         conn=pymysql.connect(host='192.168.3.232',user='zwj',passwd='123456',db='caiji',charset='utf8',port=3306)
#         cursor=conn.cursor()

#         #在数据库中添加数据，违反唯一性约束则不插入
#         sql_insert="insert into HLJ_QYNEWS(PRIPID,TITLE,SITE,URL,FBRQ,XWNR,bs)" \
#                    "values('%s','%s','%s','%s','%s','%s',%d)" % (item['pripid'],item['title'],item['site'],item['url'],item['fbrq'],item['xwnr'],213)
#         cursor.execute(
# sql_insert)
#         conn.commit()
#         #断开数据库的链接
#         cursor.close()
#         conn.close()

        return item
