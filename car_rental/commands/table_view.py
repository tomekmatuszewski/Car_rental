from prettytable import PrettyTable
from car_rental.control.data_access import Base


def set_table_with_headers(table_db: Base, tables: dict) -> PrettyTable:
    table = PrettyTable()
    table.field_names = tables[table_db].columns
    return table
