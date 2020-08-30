from sqlalchemy import inspect
from car_rental.control.utils import *
from car_rental.models.client import Countries, Cities, Clients
from car_rental.models.car import CarTypes, CarItems, Cars
from car_rental.models.order import Orders
from car_rental.control.data_access import Base
from prettytable import PrettyTable


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

    def get_table(self, table_db):
        return self.tables[table_db]

    @staticmethod
    def create_row(table: Base) -> dict:
        return {
            c.key: getattr(table, c.key) for c in inspect(table).mapper.column_attrs
        }

    @staticmethod
    def add_row(session, input_data: str, table: Base) -> None:
        data = parse_data(input_data, table.columns)
        session.add(table(**data))
        session.commit()

    def update_row(self, session, tabledb: str, row: int, column: str, value: str) -> None:
        table = self.tables[tabledb]
        session.query(table).filter(table.id == row).update({column: value})
        session.commit()

    def delete_table_row(self, session, tabledb: Base, row: int) -> None:
        table = self.tables[tabledb]
        session.query(table).filter(table.id == row).delete()
        session.commit()

    def show_dbtable(self, query, table):
        ptable = set_table_with_headers(table.columns)
        if not query.all():
            return msg_obj_notibdb()
        for row in query:
            ptable.add_row(list(self.create_row(row).values()))
        return ptable

    def search_all_row(self, session, table_db: str):
        table = self.get_table(table_db)
        query = session.query(table)
        return self.show_dbtable(query, table)

    def search_selected_row(self, session, table_db: str, column: str, value: str):
        table = self.get_table(table_db)
        query = session.query(table).filter_by(**{column: value})
        return self.show_dbtable(query, table)
