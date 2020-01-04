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
    domain = 'http://www.shenliancaijing.com'
    allowed_domains = ['shenliancaijing.com']

    def start_requests(self):
        post_url = 'https://www.shenliancaijing.com/api/express/get'
        # id=0&channel=1&is_content=1&pn=1&lastdate=&from=pc
        formdata = {
            'id': "0",
            'channel': "1",
            'is_content': "1",
            'pn': "1",
            'from': 'pc'
        }
        # yield scrapy.Request(url=post_url, method='POST', body=json.dumps(formdata), callback=self.parse, headers={'Content-Type':'application/json'})
        yield scrapy.FormRequest(url=post_url, formdata=formdata, callback=self.parse)

    def parse(self, response):
        site_name = '深链财经'
        crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news_list = []
        ret_json = json.loads(response.body)
        print(json.dumps(ret_json))
        news_list = ret_json['data']['list']
        for news in news_list:
            # print(news)
            item = BeepCrawlerItem()
            item['title'] = news['title']
            item['content'] = news['content']
            item['source'] = ''
            item['link'] = self._get_link_detail(news)
            item['published_at'] = datetime.fromtimestamp(news['createtime']/1e3).strftime('%Y-%m-%d %H:%M:%S')
            item['crawled_at'] = crawled_at
            item['site_name'] = site_name
            item['md5_content'] = hashlib.md5(item['link'].encode('utf8')).hexdigest()
            print(item)
            yield item

    def _get_link_detail(self, news):
        link_detail = self.domain + '/a/' + str(news['id']) + '.html'
        return link_detail
        

