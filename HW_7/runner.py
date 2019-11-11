from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from zillow import settings
from zillow.spiders.zillow import ZillowSpider

if __name__ == '__main__':
    crawler_settings = Settings()  # Инициализацтя настроек crawler
    crawler_settings.setmodule(settings)

    town_list = ['mcgrath-ak', 'tok-ak']

    process = CrawlerProcess(settings=crawler_settings)  # Создаем процесс
    process.crawl(ZillowSpider, town_list)  # Добавляем пауков
    process.start()
