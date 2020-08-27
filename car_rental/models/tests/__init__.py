from sqlalchemy import create_engine
from models import Base
import pytest
from sqlalchemy.orm import sessionmaker


class Database:

    engine = None
    conn_string = None

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string, echo=False)
        Base.metadata.create_all(self.engine)

    @staticmethod
    def create_objects(db_obj, levels_data):
        return [db_obj(**level) for level in levels_data]

    def add_obj(self, level, level_data, session):
        session.add_all(self.create_objects(level, level_data))
        session.commit()


@pytest.fixture(scope="module", name="db")
def create_db():
    db = Database()
    db.db_init("sqlite:///:memory:")
    return db


@pytest.fixture(scope="module", name="session")
def create_session(db):
    Session = sessionmaker(bind=db.engine)
    return Session()
