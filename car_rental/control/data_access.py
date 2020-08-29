from sqlalchemy.ext.declarative import declarative_base
from car_rental.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class DataAccess:
    def __init__(self):
        self.engine = None
        self.conn_string = Config.SQLALCHEMY_DATABASE_URI
        self.session = None

    def connect(self) -> None:
        self.engine = create_engine(self.conn_string, echo=False)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
