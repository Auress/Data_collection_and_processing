# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class AvitoCarsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def photo_cleaner(urls):
    if urls[:2] == '//':
        return f'http:{urls}'
    return urls


def params_cleaner(item):
    key = item.split('">')[-1].split(':')[0]
    value = item.split('">')[-1].split(':')[-1].split('</span>')[-1].split('</li>')[0]
    return {key: value}


def params_dict(items):
    result = {}
    for x in items:
        result.update(x)
    return result


class AvitoCars(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(params_cleaner), output_processor=params_dict)
    photos = scrapy.Field(input_processor=MapCompose(photo_cleaner))
    json_car_spec = scrapy.Field()
    json_VIN_db = scrapy.Field()
