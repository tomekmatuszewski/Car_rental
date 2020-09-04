from typing import Dict, List

from prettytable import PrettyTable


def set_table_with_headers(columns: list) -> PrettyTable:
    table = PrettyTable()
    table.field_names = columns
    return table


def parse_data(data: str, columns: List) -> Dict:
    lst_data = data.split(",")
    return {k: v for k, v in zip(columns, lst_data)}


def msg_empty_table(table):
    return f"Searched table {str(table.__table__).capitalize()} is empty"
