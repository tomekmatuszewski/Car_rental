import typer
from prettytable import PrettyTable
from car_rental.control.create_db import Database
from car_rental.models.client import Countries, Cities, Clients
from car_rental.models.car import CarTypes, CarItems, Cars
from car_rental.models.order import Orders

app = typer.Typer()
db = Database()
db.start_db()

tables = {"Cities": Cities, "Countries": Countries, "Clients": Clients,
          "CarTypes": CarTypes, "CarItems": CarItems, "Cars": Cars,
          "Orders": Orders}


@app.command()
def add_data(table_db: str):
    pass


@app.command()
def show_database(table_db: str):
    table = PrettyTable()
    table.field_names = tables[table_db].columns

    typer.echo(table)


if __name__ == "__main__":
    show_database("Clients")