from sqlalchemy import inspect
from car_rental.control.utils import *
from car_rental.models.client import Countries, Cities, Clients
from car_rental.models.car import CarTypes, CarItems, Cars
from car_rental.models.order import Orders


class ControlDb:

    tables = {
        "Cities": Cities,
        "Countries": Countries,
        "Clients": Clients,
        "CarTypes": CarTypes,
        "CarItems": CarItems,
        "Cars": Cars,
        "Orders": Orders,
    }

    @staticmethod
    def create_row(table):
        return {
            c.key: getattr(table, c.key) for c in inspect(table).mapper.column_attrs
        }

    @staticmethod
    def add_row(session, input_data: str, table):
        data = parse_data(input_data, table.columns)
        session.add(table(**data))
        session.commit()

    @staticmethod
    def update_row(session, table, row: int, column: str, value: str):
        session.query(table).filter(table.id == row).update({column: value})
        session.commit()

    @staticmethod
    def delete_row(session, table, row: int):
        session.query(table).filter(table.id == row).delete()
        session.commit()
