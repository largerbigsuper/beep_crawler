# -*- coding: utf-8 -*-
import scrapy


class A8btcSpider(scrapy.Spider):
    name = '8btc'
    allowed_domains = ['https://www.8btc.com/']
    start_urls = ['https://www.bishijie.com/kuaixun']

    def parse(self, response):
        pass
