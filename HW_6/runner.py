from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from insta import settings
from insta.spiders.instagram import InstagramSpider
from config import INSAT_LOGIN, INSAT_PASS

if __name__ == '__main__':
    crawler_settings = Settings()  # Инициализацтя настроек crawler
    crawler_settings.setmodule(settings)

    insta_parse_list = ['masjidtrans.id', 'aherlam']  # 'motsdouxetinfinis', 'masjidtrans.id', 'lisajolampi', 'aherlam']

    process = CrawlerProcess(settings=crawler_settings)  # Создаем процесс
    process.crawl(InstagramSpider, INSAT_LOGIN, INSAT_PASS, insta_parse_list)  # Добавляем пауков
    process.start()
