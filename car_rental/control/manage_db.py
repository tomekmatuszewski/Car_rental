from sqlalchemy import create_engine
from car_rental.models import Base
from sqlalchemy.orm import sessionmaker
from car_rental.config import Config


class Database:

    engine = None

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string, echo=False)
        Base.metadata.create_all(self.engine)

    @staticmethod
    def create_db():
        db = Database()
        db.db_init(Config.SQLALCHEMY_DATABASE_URI)
        return db

    @staticmethod
    def create_session(db):
        session = sessionmaker(bind=db.engine)
        return session()

    def start_db(self):
        self.create_session(self.create_db())


    def add_row(self):

    # @staticmethod
    # def create_objects(db_obj, levels_data):
    #     return [db_obj(**level) for level in levels_data]
    #
    # def add_obj(self, level, level_data, session):
    #     session.add_all(self.create_objects(level, level_data))
    #     session.commit()


