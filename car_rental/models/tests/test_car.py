import pytest
from sqlalchemy import func
from car_rental.models.car import CarTypes, Cars, CarItems
from car_rental.models.order import Orders
from car_rental.models.client import Clients
from car_rental.models.tests import TestDbMethods
from car_rental.control.data_access import DataAccess


@pytest.fixture(scope="module", name="dl")
def connect_db():
    dl = DataAccess()
    dl.conn_string = "sqlite:///:memory:"
    dl.connect()
    return dl


@pytest.fixture(scope="module", name="session")
def start_session(dl):
    session = dl.session()
    return session


@pytest.fixture(scope="module", name="db")
def db_method():
    return TestDbMethods()


def test_car_type(session, db):
    car_type_data = ({"type_name": "truck"}, {"type_name": "car"})
    db.add_obj(CarTypes, car_type_data, session)
    assert session.query(func.count("*")).select_from(CarTypes).scalar() == 2
    assert session.query(CarTypes)[0].type_name == "truck"


def test_car(session, db):
    car_data = (
        {"model": "Corolla", "brand": "Toyota"},
        {"model": "I30", "brand": "Hyundai"},
        {"model": "A4", "brand": "Audi"},
        {"model": "A6", "brand": "Audi"},
    )
    db.add_obj(Cars, car_data, session)
    assert session.query(func.count("*")).select_from(Cars).scalar() == 4
    assert session.query(Cars)[0].model == "Corolla"
    assert session.query(Cars)[2].brand == "Audi"
    assert session.query(func.count("*"), Cars.brand).group_by(Cars.brand).order_by(
        Cars.brand
    ).all()[0] == (2, "Audi")
    assert session.query(Cars.brand).distinct().count() == 3


def test_car_item(session, db):
    car_item_data = (
        {
            "car_id": 1,
            "car_type_id": 2,
            "price_per_day": 22.50,
            "production_year": "2016",
            "engine": "1.6 Turbo",
            "fuel": "petrol",
            "availability": 1,
        },
        {
            "car_id": 3,
            "car_type_id": 2,
            "price_per_day": 15.00,
            "production_year": "2015",
            "engine": "2.0 TDI",
            "fuel": "diesel",
            "availability": 0,
        },
    )
    db.add_obj(CarItems, car_item_data, session)
    assert session.query(func.count("*")).select_from(CarItems).scalar() == 2
    assert session.query(CarItems)[0].production_year == "2016"
    assert session.query(CarItems)[0].car.brand == "Toyota"
    assert not session.query(CarItems).filter(CarItems.price_per_day < 10).all()
    assert len(session.query(Cars)[0].car_item) == 1


def test_car_item2(session, db):
    car_item_data = (
        {
            "car_id": 1,
            "car_type_id": 2,
            "price_per_day": 100.50,
            "production_year": "2016",
            "engine": "1.6 Turbo",
            "fuel": "petrol",
            "availability": 2,
        },
    )
    with pytest.raises(AssertionError):
        db.add_obj(CarItems, car_item_data, session)
