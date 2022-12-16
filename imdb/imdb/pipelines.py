# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class ImdbPipeline:

    def __init__(self):
        self.conn = MongoClient("localhost:27017")
        db = self.conn.scrapyPipeline
        self.movies = db.movies

    def process_item(self, item, spider):
        self.movies.insert_one(dict(item))
        return item

class ImdbSeriePipeline:

    def __init__(self):
        self.conn = MongoClient("localhost:27017")
        db = self.conn.scrapyPipeline
        self.serie = db.serie

    def process_item(self, item, spider):
        self.serie.insert_one(dict(item))
        return item