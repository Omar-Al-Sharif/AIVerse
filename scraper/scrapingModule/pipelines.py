# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re
import sys

import pymongo
from dateutil import parser

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapingModule.items import Article
from scrapy.exceptions import DropItem
from unidecode import unidecode


class ScrapingmodulePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["title"] = unidecode(adapter["title"][0].strip().replace("\f\n\r\t\v", ""))
        adapter["content"] = re.sub(" +", " ", unidecode(adapter["content"][0].strip().replace("\n", "")))

        adapter["published_time"] = parser.isoparse(adapter["published_time"])
        adapter["modified_time"] = parser.isoparse(adapter["modified_time"])

        return item


class MongoDBPipeline:
    collection = "scrapy_items"

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri:
            sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get("MONGODB_URI"),
            mongodb_db=crawler.settings.get("MONGODB_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(Article(item))
        exist = self.db[self.collection].find_one(data)
        if exist:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.db[self.collection].insert_one(data)
        return item
