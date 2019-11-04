# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Avito_cars.items import AvitoCars
import json


class CarsInfoSpider(scrapy.Spider):
    name = 'cars_info'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili/']

    def parse(self, response: HtmlResponse):
        cars_page = response.css('div.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended '
                                 'a.item-description-title-link ::attr(href)').extract()

        for x in cars_page:
            yield response.follow(x, callback=self.parse_page)

        pagination = response.css('div.pagination.js-pages a.pagination-page.js-pagination-next ::attr(href)'
                                  ).extract_first()
        yield response.follow(pagination, callback=self.parse)

    def parse_page(self, response: HtmlResponse):
        item = ItemLoader(AvitoCars(), response)
        item.add_css('title', 'span.title-info-title-text ::text')
        item.add_css('price', 'span.js-item-price  ::attr(content)')
        item.add_css('params', 'li.item-params-list-item')
        item.add_css('photos', 'div.gallery-img-frame.js-gallery-img-frame ::attr(data-url)')

        page_id = response.url.split('_')[-1]
        url_car_spec = f'https://www.avito.ru/js/items/{page_id}/car_spec'

        yield response.follow(url_car_spec, callback=self.parse_car_spec, cb_kwargs={'item': item, 'page_id': page_id})

    def parse_car_spec(self, response: HtmlResponse, item, page_id):
        json_car_spec = json.loads(response.body_as_unicode())
        item.add_value('json_car_spec', json_car_spec)
        url_VIN_db = f'https://www.avito.ru/web/1/swaha/v1/autoteka/teaser/{page_id}'
        yield response.follow(url_VIN_db, callback=self.parse_VIN_db, cb_kwargs={'item': item, 'page_id': page_id})

    def parse_VIN_db(self, response: HtmlResponse, item, page_id):
        json_VIN_db = json.loads(response.body_as_unicode())
        item.add_value('json_VIN_db', json_VIN_db)
        yield item.load_item()
