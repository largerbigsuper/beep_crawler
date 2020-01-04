# -*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime

import scrapy

from beep_crawler.items import BeepCrawlerItem


class OdailySpider(scrapy.Spider):
    name = 'odaily'
    domain = 'https://www.odaily.com'
    allowed_domains = ['odaily.com']
    start_urls = ['https://www.odaily.com/api/pp/api/info-flow/newsflash_columns/newsflashes?b_id=&per_page=20']

    def parse(self, response):
        site_name = '星球日报'
        crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news_list = []
        ret_json = json.loads(response.body)
        news_list = ret_json['data']['items']
        for news in news_list:
            item = BeepCrawlerItem()
            item['title'] = news['title']
            item['content'] = news['description']
            item['source'] = ''
            item['link'] = self._get_link_detail(news)
            item['published_at'] = news['published_at']
            item['crawled_at'] = crawled_at
            item['site_name'] = site_name
            item['md5_content'] = hashlib.md5(item['link'].encode('utf8')).hexdigest()
            # print(item)
            yield item

    def _get_link_detail(self, news):
        link_detail = self.domain + '/newsflash/' + str(news['id'])
        return link_detail
        
