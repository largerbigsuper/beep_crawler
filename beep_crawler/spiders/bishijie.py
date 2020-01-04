# -*- coding: utf-8 -*-
import time
import json
from datetime import datetime
import hashlib

import scrapy

from beep_crawler.items import BeepCrawlerItem

class BishijieSpider(scrapy.Spider):
    name = 'bishijie'
    domain = 'https://www.bishijie.com'
    allowed_domains = ['bishijie.com']
    start_urls = [domain]


    def parse(self, response):
        site_name = '币世界'
        crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news_list = []
        li_list = response.xpath('//ul[@class="newscontainer"]//li')
        for news in li_list:
                item = BeepCrawlerItem()
                item['title'] = self._get_title(news)
                item['content'] = self._get_content(news)
                item['source'] = ''
                item['link'] = self._get_link_detail(news)
                item['published_at'] = crawled_at
                item['crawled_at'] = crawled_at
                item['site_name'] = site_name
                item['md5_content'] = hashlib.md5(item['link'].encode('utf8')).hexdigest()

                yield item

    def _get_title(self, news):
        title = news.xpath('.//h3/text()').extract_first().strip()
        return title

    def _get_content(self, news):
        content = news.xpath('.//div[@class="h63"]/text()').extract_first().strip() 
        return content

    def _get_link_detail(self, news):
        link_detail = news.xpath('.//a/@href').extract_first().strip()
        return self.domain + link_detail