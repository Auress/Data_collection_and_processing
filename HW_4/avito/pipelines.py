# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
from sql_avito_database import AvitoBase
from sql_avito_tables import Real_estate, Media, Author, Base_avito


class AvitoPipeline(object):
    def __init__(self):
        db_url = 'sqlite:///Avito_base.sqlite'
        self.db = AvitoBase(Base_avito, db_url)

    def process_item(self, item, spider):
        self.db.session.autocommit=True

        author = Author(item.get('author'))
        try:
            self.db.session.add(author)
        finally:
            author = self.db.session.query(sqlalchemy.select([Author.id]).where(
                Author.url_author == item.get('author')))[0][0]

        Real_estate_ins = Real_estate(item.get('title'), item.get('url_ad'), float(item.get('price')),
                                      item.get('flat_address'), author)
        try:
            self.db.session.add(Real_estate_ins)
        finally:
            ad_id = self.db.session.query(sqlalchemy.select([Real_estate.id]).where(
                Real_estate.url_ad == item.get('url_ad')))[0][0]

        for x in item.get('media'):
            media_ins = Media(ad_id, x)
            self.db.session.add(media_ins)

        return item
