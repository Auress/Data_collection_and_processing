# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class AvitoCarsPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        avito_cars_data_base = client.Avito_cars
        self.avito_cars_collection = avito_cars_data_base.avito_cars

    def process_item(self, item, spider):
        self.avito_cars_collection.insert_one(item._values)
        return item


class AvitoPhotosPipelines(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for image_file in item['photos']:
                try:
                    yield scrapy.Request(image_file)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [x[1] for x in results if x[0]]
        return item
