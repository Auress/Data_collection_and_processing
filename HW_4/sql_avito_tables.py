# coding: UTF-8
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Float)
from sqlalchemy.ext.declarative import declarative_base

Base_avito = declarative_base()
# Недвижимость Квартиры
# Название, Ссылки на все фото, Стоимость, URL объявления, URL автора объявления, Адрес местоположения объекта


class Real_estate(Base_avito):
    __tablename__ = 'real_estate'

    # Создаем колонки
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url_ad = Column(String, unique=True)
    price = Column(Float)
    flat_address = Column(String)
    author = Column(Integer, ForeignKey('author.id'))

    def __init__(self, name, url_ad, price, flat_address, author):
        self.name = name
        self.url_ad = url_ad
        self.price = price
        self.flat_address = flat_address
        self.author = author


class Media(Base_avito):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(Integer, ForeignKey('real_estate.id'))
    url_media = Column(String)

    def __init__(self, owner, url_media):
        self.owner = owner
        self.url_media = url_media


class Author(Base_avito):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url_author = Column(String, unique=True)

    def __init__(self, url_author):
        self.url_author = url_author
