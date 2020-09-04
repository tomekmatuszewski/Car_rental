from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from car_rental.config import Config

Base = declarative_base()


class DataAccess:
    def __init__(self):
        self.engine = None
        self.conn_string = Config.SQLALCHEMY_DATABASE_URI
        self.session = None
        self.base = Base

    def connect(self) -> None:
        self.engine = create_engine(self.conn_string, echo=False)
        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
