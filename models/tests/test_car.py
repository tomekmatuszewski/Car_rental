import pytest
from sqlalchemy import func
from models.car import CarTypes, Cars, CarItems
from models.tests import create_db, create_session


@pytest.fixture(scope="module")
def start_fixture():
    create_session(create_db())


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
    assert session.query(func.count("*"), Cars.brand).group_by(Cars.brand).order_by(Cars.brand).all()[0] == (2, "Audi")
    assert session.query(Cars.brand).distinct().count() == 3