# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import datetime
import logging

import pymysql
import environs


env = environs.Env()
env.read_env('.env')

DB_CONFIG = {
    'host': env('DB_HOST'),
    'user': env('DB_USER'),
    'password': env('DB_PASSWORD'),
    'db': env('DB_NAME'),
    'port': env.int('DB_PORT'),
    'charset': 'utf8mb4',
}

class BeepCrawlerPipeline(object):

    def __init__(self, *args, **kwargs):
        self.db = pymysql.connect(**DB_CONFIG)
        self.logger = logging.getLogger('pipeline')

        with self.db.cursor() as cursor:
            three_day_ago = datetime.datetime.now() - datetime.timedelta(days=3)
            crawled_at = three_day_ago.strftime('%Y-%m-%d')
            sql = 'SELECT md5_content FROM crawled_document WHERE crawled_at > {};'.format(
                crawled_at)
            cursor.execute(sql)
            crawled_md5 = {q[0] for q in cursor.fetchall()}
        self.crawled_md5_set = crawled_md5

    def process_item(self, item, spider):
        # 去重
        if item['md5_content'] in self.crawled_md5_set:
            return
            
        with self.db.cursor() as cursor:
            sql = '''INSERT INTO crawled_document 
            (title, content, source, link, published_at, crawled_at, site_name, md5_content, is_news) 
            VALUES 
            ('{title}', '{content}', '{source}', '{link}', '{published_at}', '{crawled_at}', '{site_name}', '{md5_content}', 0);
            '''.format(**item)
            self.logger.info(sql)

            cursor.execute(sql)
        self.db.commit()

        return item
