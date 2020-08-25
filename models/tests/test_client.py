import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models.client import Countries, Cities, Clients
from models import Base


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


def test_country(session, db):
    COUNTRY_DATA = ({"name": "Poland"}, {"name": "Great Britain"})
    db.add_obj(Countries, COUNTRY_DATA, session)
    assert session.query(func.count("*")).select_from(Countries).scalar() == 2
    assert session.query(Countries)[0].name == "Poland"


def test_city(session, db):
    city_data = (
        {"name": "Warsaw", "country_id": 1},
        {"name": "London", "country_id": 2},
    )
    db.add_obj(Cities, city_data, session)
    assert session.query(func.count("*")).select_from(Cities).scalar() == 2
    assert session.query(Cities)[0].name == "Warsaw"
    assert session.query(Cities)[0].country.name == "Poland"


def test_client(session, db):
    client_data = (
        {
            "first_name": "Joe",
            "last_name": "Doe",
            "pesel_number": "91020516344",
            "address": "Churchil street 2, London",
            "email": "joe.doe@yahoo.com",
            "city_id": 2,
        },
        {
            "first_name": "Jan",
            "last_name": "Nowak",
            "pesel_number": "80121089256",
            "address": "ul. Zygmuntowska 2, 00-222 Warszawa",
            "email": "jan.nowak@gmail.com",
            "city_id": 1,
        },
    )
    db.add_obj(Clients, client_data, session)
    assert session.query(func.count("*")).select_from(Clients).scalar() == 2
    assert session.query(Clients)[0].pesel_number == "91020516344"
    assert session.query(Clients)[0].full_name == "Joe Doe"
    assert session.query(Clients)[0].city.name == "London"
    assert (
        session.query(Clients.email).filter_by(id=2).all()[0][0]
        == "jan.nowak@gmail.com"
    )


def test_client2(session, db):
    client_data = (
        {
            "first_name": "Joe",
            "last_name": "Doe",
            "pesel_number": "91020516344",
            "address": "Churchil street 2, London",
            "email": "joe.doeyahoo.com",
            "city_id": 2,
        },
    )
    with pytest.raises(AssertionError):
        db.add_obj(Clients, client_data, session)
