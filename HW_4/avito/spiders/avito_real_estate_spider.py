# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class AvitoRealEstateSpider(scrapy.Spider):
    name = 'avito_real_estate'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry/']

    def parse(self, response: HtmlResponse):
        real_estate_page = response.xpath("//div[contains(@class, 'item item_table clearfix')]//a[contains("
                                          "@class, 'item-description-title-link')]/@href").extract()
        for x in real_estate_page:
            yield response.follow(x, callback=self.parse_page)

        paginator = response.xpath("//div[contains(@class, 'pagination-nav clearfix')]"
                                   "//a[contains(@class, 'pagination-page js-pagination-next')]/@href").extract_first()
        yield response.follow(paginator, callback=self.parse)

    def parse_page(self, response: HtmlResponse):
        title = response.xpath("//div[contains (@class, 'item-view-content')]//span[@itemprop='name']"
                              "/text()").extract_first()
        price = response.xpath("//div[contains (@class, 'item-view-price js-item-view-price')]"
                               "//span[contains (@class, 'js-item-price')]/@content").extract_first()
        flat_address = response.xpath("//span[contains (@class, 'item-address__string')]/text()").extract_first()
        url_ad = response.url
        author = response.xpath("//div[contains (@class, 'item-view-seller-info js-item-view-seller-info')]"
                                "//div[contains (@class, 'seller-info-name js-seller-info-name')]/a/@href"
                                ).extract_first()
        media = response.xpath('//div[contains (@class, "js-gallery-img-frame")]//@data-url').extract()

        item = {'title': title,
                'price': price,
                'flat_address': flat_address,
                'url_ad': url_ad,
                'author': author,
                'media': media}

        yield item
