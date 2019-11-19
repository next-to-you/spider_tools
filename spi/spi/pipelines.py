# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import json
from scrapy.exporters import CsvItemExporter, ScrapyJSONEncoder, JsonItemExporter
import pymongo
import redis


class AqiDataPipeline(object):
    def process_item(self, item, spider):
        item['data_source'] = spider.name
        item['data_time'] = datetime.now()
        return item


# # 存储json的管道
class SpiJsonPipeline(object):
    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def open_spider(self, spider):
        self.filename = open("aqi_json.json", "wb")
        self.writer = JsonItemExporter(self.filename)
        self.writer.start_exporting()

    def close_spider(self, spider):
        self.filename.close()


# # csv 存储的管道
class SpiCsvPipeline(object):
    def process_item(self, item, spider):
        self.csv_write.export_item(item)
        return item

    def open_spider(self, spider):
        self.file_csv_name = open('api_csv.csv', 'wb')
        self.csv_write = CsvItemExporter(self.file_csv_name)
        self.csv_write.start_exporting()

    def close_spider(self, spider):
        self.csv_write.finish_exporting()
        self.file_csv_name.close()


# 存储mongodb 的数据库
class SpiMongoPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client['AQI']
        self.collection = self.db['day']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


# # 存储redis 的数据库
class AqiRedisPipeline(object):

    def open_spider(self, spider):
        self.redis_client = redis.Redis(host="127.0.0.1", port=6379)
        self.save_key = 'aqi_redis'

    def process_item(self, item, spider):
        self.redis_client.lpush(self.save_key, str(item))
        # content = json.dumps(dict(item))
        # self.redis_client.lpush('AQI_REDIS_LIST', content)

        return item
