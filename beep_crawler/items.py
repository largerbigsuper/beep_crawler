# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeepCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    site_name = scrapy.Field() # 网站名
    title = scrapy.Field() # 标题
    content = scrapy.Field() # 内容
    published_at = scrapy.Field() # 发布时间
    source = scrapy.Field() # 爬取原始平台
    link = scrapy.Field() # 原始链接
    crawled_at = scrapy.Field() # 爬取时间
    md5_content = scrapy.Field() # 爬取时间



