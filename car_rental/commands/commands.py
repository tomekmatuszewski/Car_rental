import typer
from car_rental.control.manage_db import ControlDb
from car_rental.commands.table_view import set_table_with_headers
from car_rental.control.data_access import DataAccess
from car_rental.commands.utils import *


app = typer.Typer()
dal = DataAccess()
dal.connect()
session = dal.session()
db = ControlDb()


@app.command()
def insert_row(table_db: str) -> None:
    show_table(table_db)
    table = db.tables[table_db]
    data = enter_data(table)
    db.add_row(session, data, table)


@app.command()
def show_table(table_db: str) -> None:
    table = set_table_with_headers(table_db, db.tables)
    query = session.query(db.tables[table_db])
    for row in query:
        table.add_row(list(db.create_row(row).values()))
    typer.echo(table)


@app.command()
def update_table(table_db: str, row: int, column: str, value: str) -> None:
    show_table(table_db)
    table = db.tables[table_db]
    db.update_row(session, table, row, column, value)
    show_table(table_db)


@app.command()
def delete_row(table_db: str, row: int) -> None:
    table = db.tables[table_db]
    db.delete_row(session, table, row)


# @app.command()
# def search_row(table_db: str, row: int):
#     table = db.tables[table_db]
#     db.search_row(session, table, row)



