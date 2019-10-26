from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avito import settings
from avito.spiders.avito_real_estate_spider import AvitoRealEstateSpider

if __name__ == '__main__':
    crawler_settings = Settings()  # Инициализацтя настроек crawler
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)  # Создаем процесс
    process.crawl(AvitoRealEstateSpider)  # Добавляем пауков
    process.start()

    print(1)
