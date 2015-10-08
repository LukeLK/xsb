# -*- coding: utf-8 -*-

__author__ = 'bitfeng'
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
import sys
import datetime
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
reload(sys)
sys.setdefaultencoding('utf-8')


# class MySQLPipeline(object):
#
#     def __init__(self):
#         self.dbpool = adbapi.ConnectionPool(
#             'MySQLdb',
#             db='xsbcc',
#             user='root',
#             passwd='wybigdata',
#             cursorclass=MySQLdb.cursors.DictCursor,
#             charset='utf8',
#             use_unicode=True)
#
#     def process_item(self, item, spider):
#         # run db query in thread pool
#         query = self.dbpool.runInteraction(self._conditional_insert, item)
#         query.addErrback(self.handle_error)
#
#         return item
#
#     def _conditional_insert(self, tx, item):
#         # create record if doesn't exist.
#         # all this block run on it's own thread
#         tx.execute("select * from websites where link = %s", (item['link'][0], ))
#         result = tx.fetchone()
#         if result:
#             log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
#         else:
#             tx.execute(\
#                 "insert into websites (link, created) "
#                 "values (%s, %s)",
#                 (item['link'][0],
#                  datetime.datetime.now())
#             )
#             log.msg("Item stored in db: %s" % item, level=log.DEBUG)
#
#     def handle_error(self, e):
#         log.err(e)


# 格式转换
class FormatItemPipeline(object):

    def process_item(self, item, spider):
        for key in item.keys():
            if type(item[key]) == list:  # 将list转换为string，并去掉\n
                if len(item[key]) == 0:
                    item[key] = 'null'
                elif len(item[key]) == 1:
                    item[key] = ''.join(''.join(item[key]).split())
                else:
                    item[key] = ''.join('|'.join(item[key]).split())
            # elif type(item[key] == str):  # 去掉string的\n
            #     item[key] = '/'.join(item[key].split())
            else:
                pass
        return item


# json格式，写json文件
class JsonWriterPipeline(object):

    # 初始化
    def __init__(self):
        pass

    # 打开spider，同时打开json文件
    def open_spider(self, spider):
        self.file_xsb = open(spider.name+'-xsbcc-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_compro = open(spider.name+'-comPro-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_senior = open(spider.name+'-senior-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_histEvo= open(spider.name+'-histEvo-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_equSta = open(spider.name+'-equSta-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_finInd = open(spider.name+'-finInd-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')

    # 关闭spider，同时关闭json文件
    def close_spider(self, spider):
        self.file_xsb.close()
        self.file_compro.close()
        self.file_senior.close()
        self.file_histEvo.close()
        self.file_equSta.close()
        self.file_finInd.close()

    # 处理spider返回的item，写的json文件
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if item.class_name() == 'XsbccItem':
            self.file_xsb.write(line)
        elif item.class_name() == 'CompanyProfile':
            self.file_compro.write(line)
        elif item.class_name() == 'SeniorExecutive':
            self.file_senior.write(line)
        elif item.class_name() == 'HistoricalEvolution':
            self.file_histEvo.write(line)
        elif item.class_name() == 'EquityStatus':
            self.file_equSta.write(line)
        elif item.class_name() == 'FinancialIndex':
            self.file_finInd.write(line)
        else:
            pass
        return item
