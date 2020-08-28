import pytest
from car_rental.control.data_access import DataAccess
from car_rental.control.manage_db import ControlDb
from car_rental.models.car import Cars, CarTypes, CarItems
from car_rental.models.order import Orders
from car_rental.models.client import Cities, Countries, Clients


@pytest.fixture(scope="module", name="db")
def connect_db():
    db = DataAccess()
    db.conn_string = "sqlite:///:memory:"
    db.connect()
    return db


@pytest.fixture(scope="module", name="session")
def start_session(db):
    session = db.session()
    return session


def test_insert_row(session):
    ControlDb.add_row(session, "1,Toyota,Corolla", Cars)
    assert session.query(Cars)[0].brand == "Toyota"
    assert session.query(Cars)[0].model == "Corolla"
    assert session.query(Cars)[0].id == 1


def test_create_row(session):
    query = session.query(Cars)
    for row in query:
        assert ControlDb.create_row(row) == {
            "id": 1,
            "brand": "Toyota",
            "model": "Corolla",
        }


def test_update_row(session):
    ControlDb.update_row(session, Cars, 1, "model", "Avensis")
    ControlDb.update_row(session, Cars, 1, "brand", "Toyota 1")
    assert session.query(Cars)[0].model == "Avensis"
    assert session.query(Cars)[0].brand == "Toyota 1"


def test_delete_row(session):
    ControlDb.add_row(session, "2,Toyota,Avensins", Cars)
    ControlDb.add_row(session, "3,Pugueot,206", Cars)
    ControlDb.delete_row(session, Cars, 3)
    assert session.query(Cars.id).count() == 2
