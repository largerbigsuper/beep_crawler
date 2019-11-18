# -*- coding: utf-8 -*-
import re
import time
import json
from datetime import datetime
import hashlib

import scrapy

from beep_crawler.items import BeepCrawlerItem

class ShenliancaijingSpider(scrapy.Spider):
    name = 'shenliancaijing'
    allowed_domains = ['shenliancaijing.com']
    # start_urls = ['https://www.shenliancaijing.com/portal/message/index.html']

    def start_requests(self):
        post_url = 'https://www.shenliancaijing.com/portal/message/messageporApi'
        formdata = {
            'id': 8,
            'limit': 20,
            'page': 1
        }
        yield scrapy.Request(url=post_url, method='POST', body=json.dumps(formdata), callback=self.parse, headers={'Content-Type':'application/json'})

    def parse(self, response):
        site_name = '深链财经'
        crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news_list = []
        ret_json = json.loads(response.body)
        news_list = ret_json['data']
        for news in news_list:
            item = BeepCrawlerItem()
            post_content = scrapy.Selector(text=news['post_content'], type='html')
            print(post_content)
            span_list = post_content.xpath('//span/text()').getall()
            content = ''
            for span in span_list:
                content += span
            item['title'] = news['post_title']
            item['content'] = content
            item['source'] = news['post_source']
            item['link'] = news['url']
            item['published_at'] = datetime.fromtimestamp(news['time']/1e3).strftime('%Y-%m-%d %H:%M:%S')
            item['crawled_at'] = crawled_at
            item['site_name'] = site_name
            item['md5_content'] = hashlib.md5(item['content'].encode('utf8')).hexdigest()
            yield item
