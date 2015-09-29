# -*- coding: utf-8 -*-

import logging
import scrapy
import urllib
import codecs

from scrapy.selector import Selector

from qcwy.items import QcwyItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

keyword = "Python"
#把字符串编码成符合url规范的编码
keywordcode = urllib.quote(keyword)

is_start_page = True

class TestfollowSpider(scrapy.Spider):
   
    name = "qcwysearch"
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200%2C00&funtype=0000&industrytype=00&keyword=" + keywordcode,
    ]

    def parse(self, response):
        global is_start_page

        url = ""
        #从开始页面开始解析数据，开始页面start_urls
        if is_start_page:
            url = self.start_urls[0]
            is_start_page = False
        else:
            href = response.xpath('//table[@class="searchPageNav"]/tr/td[last()]/a/@href')
            url = response.urljoin(href.extract())

        yield scrapy.Request(url, callback=self.parse_dir_contents)
        

    def parse_dir_contents(self, response):

        for sel in response.xpath('//table[@id="resultList"]/tr[@class="tr0"]'):
            item = QcwyItem()
            temp = sel.xpath('td[@class="td1"]/a/text()').extract()
            if len(temp) > 0:
                item['title'] = temp[0] + keyword + temp[-1]
            else:
                item['title'] = keyword
            item['link'] = sel.xpath('td[@class="td1"]/a/@href').extract()[0]
            item['company'] = sel.xpath('td[@class="td2"]/a/text()').extract()[0]
            item['updatetime'] = sel.xpath('td[@class="td4"]/span/text()').extract()[0]
            yield item

        next_page = response.xpath('//table[@class="searchPageNav"]/tr/td[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_dir_contents)