# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.loader import ItemLoader
from zillow.items import Zillow_ads
from urllib.parse import urljoin
import time
import json


class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['zillow.com', 'photos.zillowstatic.com', 'zillowstatic.com']
    start_urls = ['http://zillow.com/']
    browser = webdriver.Firefox()

    def __init__(self, town_list, *args, **kwargs):
        self.town_list = town_list
        super().__init__(*args, **kwargs)

    def parse(self, response: HtmlResponse):
        for town in self.town_list:
            yield response.follow(urljoin(self.start_urls[0], town),
                                  callback=self.parse_town,
                                  cb_kwargs={'town': town})

    def parse_town(self, response: HtmlResponse, town):
        pagi = response.css('li.zsg-pagination-next ::attr(href)').extract_first()
        if pagi is not None:
            yield response.follow(pagi, callback=self.parse)

        adv_list = response.css('div.list-card-top a.list-card-link ::attr(href)').extract()
        for x in adv_list:
            yield response.follow(x, callback=self.parse_page, cb_kwargs={'town': town})

    def parse_page(self, response: HtmlResponse, town):
        item = ItemLoader(Zillow_ads(), response)
        item.add_css('title', 'div.ds-chip div.ds-price-change-address-row h1.ds-address-container ::text')
        item.add_css('params', 'ul.ds-home-fact-list li.ds-home-fact-list-item ::text')
        item.add_css('description', 'div.ds-data-col div.ds-overview-section div.Text-sc-1vuq29o-0 ::text')
        item.add_value('location', town)

        self.browser.get(response.url)

        media = self.browser.find_element_by_css_selector('.ds-media-col')
        photo_pic_img_len = len(self.browser.find_elements_by_xpath(
            '//ul[contains (@class, "media-stream")]/li/picture/source[@type="image/jpeg"]'))

        while True:
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

            images = [itm.get_attribute('srcset').split(' ')[-2] for itm in self.browser.find_elements_by_xpath(
                '//ul[contains (@class, "media-stream")]/li/picture/source[@type="image/jpeg"]')]

            tmp_len = len(self.browser.find_elements_by_xpath(
                '//ul[contains (@class, "media-stream")]/li/picture/source[@type="image/jpeg"]'))
            if photo_pic_img_len == tmp_len:
                break

            photo_pic_img_len = len(self.browser.find_elements_by_xpath(
                '//ul[contains (@class, "media-stream")]/li/picture/source[@type="image/jpeg"]'))

        item.add_value('photos', images)
        yield item.load_item()

    def __del__(self):
        self.browser.close()
