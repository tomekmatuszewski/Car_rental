from typing import List, Dict
from prettytable import PrettyTable
from car_rental.control.data_access import Base


def set_table_with_headers(columns: list) -> PrettyTable:
    table = PrettyTable()
    table.field_names = columns
    return table


def parse_data(data: str, columns: List) -> Dict:
    lst_data = data.split(",")
    return {k: v for k, v in zip(columns, lst_data)}


def msg_obj_notibdb():
    return "Searched value not in table"
