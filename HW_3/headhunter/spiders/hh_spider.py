# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class HhSpiderSpider(scrapy.Spider):
    name = 'hh_spider'
    allowed_domains = ['hh.ru']
    search = input('Enter test to search on hh.ru (default Data scientist): ') or 'Data scientist'
    start_urls = [f'https://hh.ru/search/vacancy?text={search}']

    def parse(self, response: HtmlResponse):
        hh_vacancy_page = response.css('div.vacancy-serp a.bloko-link.HH-LinkModifier ::attr(href)').extract()
        for v in hh_vacancy_page:
            yield response.follow(v, callback=self.parse_hh_vacancy_page)

        paginator = response.css(
            "div.bloko-gap.bloko-gap_top a.bloko-button.HH-Pager-Controls-Next.HH-Pager-Control").attrib.get('href')
        yield response.follow(paginator, callback=self.parse)

    def parse_hh_vacancy_page(self, response: HtmlResponse):
        title = ''.join(response.css('div.main-content h1.header ::text').extract())
        company_name = ''.join(response.css('div.bloko-columns-row a.vacancy-company-name span::text').extract())
        company_link_hh = response.css('div.vacancy-company-wrapper a.vacancy-company-name').attrib.get('href')
        salary = ''.join(response.css('div.bloko-columns-row p.vacancy-salary ::text').extract())
        skills = response.css('div.vacancy-description span::attr(data-tag-id)').extract()
        item = {'title': title,
                'company_name': company_name,
                'company_link_hh': company_link_hh,
                'salary': salary,
                'skills': skills}

        yield response.follow(company_link_hh, callback=self.parse_hh_company_page, cb_kwargs={'item': item})

    def parse_hh_company_page(self, response: HtmlResponse, item):
        item['company_link_official'] = ''.join(response.css(
            'div.bloko-columns-wrapper a.company-url').attrib.get('href'))
        yield item
