# -*- coding: utf-8 -*-
import re
import json
import hashlib
from datetime import datetime

import scrapy

from beep_crawler.items import BeepCrawlerItem


class JinseSpider(scrapy.Spider):
    name = 'jinse'
    domain = 'https://m.jinse.com'
    allowed_domains = ['api.jinse.com']
    start_urls = ['https://api.jinse.com/v4/live/list?limit=20&reading=false&source=web&sort=&flag=down&']

    def parse(self, response):
        site_name = '金色财经'
        crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news_list = []
        ret_json = json.loads(response.body)
        news_list = ret_json['list'][0]['lives']
        for news in news_list:
            item = BeepCrawlerItem()
            content = news['content']
            title = re.findall(r'【(.*)】', content)[0]
            replace = '【' + title + '】'
            item['title'] = title
            item['content'] = content.replace(replace, '')
            item['source'] = ''
            item['link'] = self._get_link_detail(news)
            item['published_at'] = datetime.fromtimestamp(news['created_at']).strftime('%Y-%m-%d %H:%M:%S')
            item['crawled_at'] = crawled_at
            item['site_name'] = site_name
            item['md5_content'] = hashlib.md5(item['link'].encode('utf8')).hexdigest()
            # print(item)
            yield item

    def _get_link_detail(self, news):
        link_detail = self.domain + '/lives/' + str(news['id']) + '.html'
        return link_detail

