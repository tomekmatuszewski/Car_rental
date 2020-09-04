import typer

from car_rental.commands.utils import *
from car_rental.control.data_access import DataAccess
from car_rental.control.manage_db import ControlDb

app = typer.Typer()
dal = DataAccess()
dal.connect()
session = dal.session()
db = ControlDb()


@app.command()
def insert_row(table_db: str) -> None:
    show_table(table_db)
    table = db.get_table(table_db)
    data = enter_data(table)
    db.add_row(session, data, table)


@app.command()
def show_table(table_db: str) -> None:
    table = db.search_all_row(session, table_db)
    typer.echo(table)


@app.command()
def update_table(table_db: str, row: int, column: str, value: str) -> None:
    show_table(table_db)
    db.update_row(session, table_db, row, column, value)
    show_table(table_db)


@app.command()
def delete_row(table_db: str, row: int) -> None:
    db.delete_table_row(session, table_db, row)


@app.command()
def search_in_table(table_db: str, column: str, value: str,) -> None:
    table = db.search_selected_row(session, table_db, column, value)
    typer.echo(table)