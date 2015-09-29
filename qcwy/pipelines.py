# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
from scrapy import signals

class QcwyJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('..\\qcwy\\qcwy\\qcwy.json', 'w', encoding = 'utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii = False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close() 

class QcwyMySQLPipeline(object):
    """docstring for MySQLPipeline"""
    def __init__(self):
        self.connpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'qcwy',
            user = 'root',
            passwd = '',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
            )
    def process_item(self, item, spider):
        query = self.connpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        if item.get('title'):
            tx.execute("insert into detail (title, link, company, updatetime) values(%s, %s, %s, %s)", 
                (item['title'], item['link'], item['company'], item['updatetime']))

    def handle_error(self, e):
        log.err(e)
