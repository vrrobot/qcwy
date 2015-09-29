# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class QcwyItem(Item):
    #定义要抓取信息的Item结构
    title       = Field()   #职位名称
    link        = Field()   #详情链接
    company     = Field()   #公司名称   
    updatetime  = Field()   #更新时间
    

