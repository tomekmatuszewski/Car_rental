from sqlalchemy import create_engine
from car_rental.models import Base
from sqlalchemy import inspect
from car_rental.control.utils import *


class Database:

    engine = None

    def db_init(self, conn_string: str):
        self.engine = create_engine(conn_string, echo=False)
        Base.metadata.create_all(self.engine)

    def create_db(self, conn_str):
        self.db_init(conn_str)

    @staticmethod
    def create_row(table):
        return {
            c.key: getattr(table, c.key) for c in inspect(table).mapper.column_attrs
        }

    @staticmethod
    def add_row(session, data: str, columns: list, table):
        data = parse_data(data, columns)
        session.add(table(**data))
        session.commit()

    @staticmethod
    def update_row(session, table, row: int, column, value):
        session.query(table).filter(table.id == row).update({column: value})
        session.commit()

    @staticmethod
    def delete_row(session, table, row: int):
        session.query(table).filter(table.id == row).delete()
        session.commit()




