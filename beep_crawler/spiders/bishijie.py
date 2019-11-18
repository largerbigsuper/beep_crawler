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
    allowed_domains = [domain]
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
                item['link'] = ''
                item['published_at'] = crawled_at
                item['crawled_at'] = crawled_at
                item['site_name'] = site_name
                item['md5_content'] = hashlib.md5(item['content'].encode('utf8')).hexdigest()
                # print(item)
                yield item

    def _get_title(self, news):
        title = news.xpath('.//h3/text()').extract_first().strip()
        return title

    def _get_content(self, news):
        content = news.xpath('.//div[@class="h63"]/text()').extract_first().strip() 
        return content




    # api_tpl = 'https://www.bishijie.com/api/newsv17/index?size={size}&client=pc&timestamp={from_timestamp}'
    # size = 100
    # from_timestamp = int(time.mktime(datetime.now().timetuple()))
    # start_url = api_tpl.format(size=size, from_timestamp=from_timestamp)
    # start_urls = [start_url]


    # def parse(self, response):
    #     site_name = '币世界'
    #     ret_json = json.loads(response.body)
    #     if ret_json['error'] != 0:
    #         return
    #     data_list = ret_json['data']
    #     for oneday_news in data_list:
    #         date = oneday_news['date']
    #         news_list = oneday_news['buttom']
    #         crawled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         for news in news_list:
    #             item = BeepCrawlerItem()
    #             item['title'] = news['title']
    #             item['content'] = news['content']
    #             item['source'] = news['source']
    #             item['link'] = news['link']
    #             item['published_at'] = datetime.fromtimestamp(news['issue_time']).strftime('%Y-%m-%d %H:%M:%S')
    #             item['crawled_at'] = crawled_at
    #             item['site_name'] = site_name
    #             item['md5_content'] = hashlib.md5(news['content'].encode('utf8')).hexdigest()
    #             # print(item)
    #             yield item


