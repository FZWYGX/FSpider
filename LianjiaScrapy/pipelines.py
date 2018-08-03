# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from traceback import format_exc
from .items import LianjiaNewItem, LianjiaErshoufangItem, LianjiaZufangItem
from .Utils_Model.init_utils import init_add_request


class LianjiaMongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        _ = spider
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['NewInfo'] .ensure_index('url', unique=True)
        self.db['EsfInfo'].ensure_index('id', unique=True)
        self.db['ZfInfo'].ensure_index('id', unique=True)

        new_items = self.db['NewInfo'].find({})
        for new_item in new_items:
            init_add_request(spider, new_item['url'])

        # er_items = self.db['EsfInfo'].find({})
        # for er_item in er_items:
        #     init_add_request(spider, er_item['url'])
        #
        # zu_items = self.db['ZfInfo'].find({})
        # for zu_item in zu_items:
        #     init_add_request(spider, zu_item['url'])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, LianjiaNewItem):
                self.db['NewInfo'].update({'url': item['url']}, {'$set': item}, upsert=True)
            elif isinstance(item, LianjiaErshoufangItem):
                self.db['EsfInfo'].update({'id': item['id']}, {'$set': item}, upsert=True)
            elif isinstance(item, LianjiaZufangItem):
                self.db['ZfInfo'].update({'id': item['id']}, {'$set': item}, upsert=True)
        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')
        except Exception as e:
            spider.logger.error(format_exc())
        return item
