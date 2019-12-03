# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class JdBookPipeline(object):

    def open_spider(self, item):
        self.file = open('asd.txt', 'w')

    def process_item(self, item, spider):
        self.file.write(str(item))
        return item

    def close_spider(self, item):
        self.file.close()


# 存储mongodb 的数据库
class SpiMongoPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017, username="python", password="python")
        self.db = self.client['AQI']
        self.collection = self.db['day']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item