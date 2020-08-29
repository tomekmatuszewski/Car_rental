from car_rental.control.data_access import Base


def enter_data(table: Base) -> str:
    data = input(
        f"Insert data to table {table.__tablename__.upper()} [use commas without spaces] {*table.columns,}: "
    )
    return data
