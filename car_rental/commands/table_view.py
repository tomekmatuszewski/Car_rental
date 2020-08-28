from prettytable import PrettyTable


def set_table_with_headers(table_db, tables):
    table = PrettyTable()
    table.field_names = tables[table_db].columns
    return table
