# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class ZillowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def get_title(item):
    return ''.join(item)


def get_params(item):
    params = dict(item[i:i+2] for i in range(0, len(item), 2))
    return params


class Zillow_ads(scrapy.Item):
    title = scrapy.Field(input_processor=get_title, output_processor=TakeFirst())
    params = scrapy.Field(input_processor=get_params)
    description = scrapy.Field(output_processor=TakeFirst())
    location = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
