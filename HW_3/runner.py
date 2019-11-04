from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from headhunter import settings
from headhunter.spiders.hh_spider import HhSpiderSpider

if __name__ == '__main__':
    crawler_settings = Settings()  # Инициализацтя настроек crawler
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)  # Создаем процесс
    process.crawl(HhSpiderSpider)  # Добавляем пауков
    process.start()
