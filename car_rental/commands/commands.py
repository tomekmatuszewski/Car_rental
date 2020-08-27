import typer
from prettytable import PrettyTable
from car_rental.control.manage_db import Database
from car_rental.control.session import create_session
from car_rental.models.client import Countries, Cities, Clients
from car_rental.models.car import CarTypes, CarItems, Cars
from car_rental.models.order import Orders
from car_rental.config import Config

app = typer.Typer()
db = Database()
db.create_db(Config.SQLALCHEMY_DATABASE_URI)
session = create_session(db)

tables = {
    "Cities": Cities,
    "Countries": Countries,
    "Clients": Clients,
    "CarTypes": CarTypes,
    "CarItems": CarItems,
    "Cars": Cars,
    "Orders": Orders,
}


@app.command()
def add_row(table_db: str):
    show_table(table_db)
    table = tables[table_db]
    table_cols = table.columns
    data = input(
        f"Insert data to table {table.__tablename__.upper()} with spaces {*table_cols,}: "
    )
    db.add_row(session, data, table_cols, table)


@app.command()
def show_table(table_db: str):
    table = PrettyTable()
    table.field_names = tables[table_db].columns
    query = session.query(tables[table_db])
    for row in query:
        table.add_row(list(db.create_row(row).values()))
    typer.echo(table)


@app.command()
def update_table(table_db: str, row: int, column: str, value):
    show_table(table_db)
    table = tables[table_db]
    db.update_row(session, table, row, column, value)
    show_table(table_db)


@app.command()
def delete_row(table_db: str, row: int):
    table = tables[table_db]
    db.delete_row(session, table, row)

