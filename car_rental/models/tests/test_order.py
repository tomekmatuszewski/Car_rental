import pytest
from sqlalchemy import func
from models.client import Clients
from car_rental.models.car import CarItems
from models.order import Orders
from car_rental.models.tests import create_session, create_db
from datetime import datetime


@pytest.fixture(scope="module")
def start_fixture():
    create_session(create_db())


def test_order(session, db):
    order_data = (
        {
            "client_id": 1,
            "car_id": 1,
            "payment_type": "credit card"
        },
        {
            "client_id": 2,
            "car_id": 2
        }
    )
    db.add_obj(Orders, order_data, session)

    assert session.query(func.count("*")).select_from(Orders).scalar() == 2
    assert session.query(Orders)[0].client_id == 1
    assert session.query(Orders)[0].payment_type == "credit card"


def test_order_with_relationship(session, db):
    client_data = (
        {
            "first_name": "Joe",
            "last_name": "Doe",
            "pesel_number": "91020516344",
            "address": "Churchill street 2, London",
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
    car_item_data = (
        {
            "car_id": 1,
            "car_type_id": 2,
            "price_per_hour": 100.50,
            "production_year": "2016",
            "engine": "1.6 Turbo",
            "fuel": "petrol",
            "availability": 1,
        },
        {
            "car_id": 3,
            "car_type_id": 2,
            "price_per_hour": 150.00,
            "production_year": "2015",
            "engine": "2.0 TDI",
            "fuel": "diesel",
            "availability": 1,
        },
    )
    order_data = (
        {
            "client_id": 1,
            "car_id": 1,
            "payment_type": "credit card"
        },
        {
            "client_id": 2,
            "car_id": 2
        }
    )

    db.add_obj(Clients, client_data, session)
    db.add_obj(CarItems, car_item_data, session)
    db.add_obj(Orders, order_data, session)

    assert session.query(Orders)[0].client.first_name == "Joe"
    assert session.query(Orders)[0].car_item.engine == "1.6 Turbo"
    assert session.query(Orders)[0].car_item.price_per_hour == 100.50
    assert session.query(Orders)[1].price is None
    assert session.query(Orders)[1].order_data_stop is None
    assert session.query(Orders)[1].order_status == "pending"


def test_order_with_relationship2(session, db):
    session.query(Orders).filter_by(id=1).update({"order_status": "finished"})
    assert session.query(Orders)[0].order_status == "finished"
    print(session.query(Orders)[0].order_data_stop)


def test_setter(session, db):
    session.query(Orders)[0].set_order_status("finished")
    assert session.query(Orders)[0].order_status == "finished"
    session.query(Orders)[0].set_order_data_stop()
    assert session.query(Orders)[0].order_data_stop == datetime.now().strftime("%d-%m-%Y %H:%M")


