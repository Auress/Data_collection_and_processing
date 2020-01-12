# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class InstaPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.instagram_data_base = client.instagram
        self.instagram_likes_collection = self.instagram_data_base.instagram_likes

    def process_item(self, item, spider):
        if self.instagram_likes_collection.name in self.instagram_data_base.list_collection_names():
            self.instagram_likes_collection.find_one_and_replace({}, item)
        else:
            self.instagram_likes_collection.insert(item)
        return item
