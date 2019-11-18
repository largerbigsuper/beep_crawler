# -*- coding: utf-8 -*-
import time
import json
from datetime import datetime
import hashlib

import scrapy

from beep_crawler.items import BeepCrawlerItem

class ChainnewsSpider(scrapy.Spider):
    name = 'chainnews'
    allowed_domains = ['chainnews.com']
    start_urls = ['https://www.chainnews.com/news/']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
        }
    }

    def parse(self, response):
        site_name = '链闻'
        crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news_list = []
        div_list = response.xpath('//div[@class="feed-item-content"]')
        print(div_list)
        for news in div_list:
                item = BeepCrawlerItem()
                item['title'] = self._get_title(news)
                item['content'] = self._get_content(news)
                item['source'] = ''
                item['link'] = ''
                item['published_at'] = crawled_at
                item['crawled_at'] = crawled_at
                item['site_name'] = site_name
                item['md5_content'] = hashlib.md5(item['content'].encode('utf8')).hexdigest()
                # print(item)
                yield item

    def _get_title(self, news):
        title = news.xpath('.//h2/a/text()').extract_first().strip() 
        return title

    def _get_content(self, news):
        content = news.xpath('.//div[@class="feed-post-summary"]/text()').extract_first().strip() 
        return content
