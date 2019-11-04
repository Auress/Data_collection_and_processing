# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class HeadhunterPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        hh_data_base = client.headhunter
        self.hh_collection = hh_data_base.hh_vacancies

    def process_item(self, item, spider):
        self.hh_collection.insert_one(item)
        return item
