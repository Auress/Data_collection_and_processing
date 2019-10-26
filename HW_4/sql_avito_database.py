# coding: UTF-8
import sqlalchemy
from sqlalchemy.orm import sessionmaker


class AvitoBase:
    def __init__(self, base, base_url):
        engine = sqlalchemy.create_engine(base_url)
        base.metadata.create_all(engine)
        session_database = sessionmaker(bind=engine)
        self.session = session_database()
