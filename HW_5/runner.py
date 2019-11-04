from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Avito_cars import settings
from Avito_cars.spiders.cars_info_spider import CarsInfoSpider

if __name__ == '__main__':
    crawler_settings = Settings()  # Инициализацтя настроек crawler
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)  # Создаем процесс
    process.crawl(CarsInfoSpider)  # Добавляем пауков
    process.start()
