import pytest
from car_rental.control.data_access import DataAccess
from car_rental.models.car import Cars, CarTypes, CarItems
from car_rental.models.order import Orders
from car_rental.models.client import Cities, Countries, Clients


@pytest.fixture(scope="module", name="dl")
def create_access():
    dl = DataAccess()
    dl.conn_string = "sqlite:///:memory:"
    dl.connect()
    return dl


@pytest.fixture(scope="module", name="session")
def start_session(dl):
    session = dl.session()
    return session


def test_data_access(session):
    assert session.query(Cars).count() == 0
    assert session.query(Orders).count() == 0
    assert session.query(Countries).count() == 0
    assert session.query(Clients).count() == 0
