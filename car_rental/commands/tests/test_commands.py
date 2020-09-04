from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from car_rental.commands.commands import app, session
from car_rental.models.car import CarItems, Cars, CarTypes
from car_rental.models.client import Cities, Clients, Countries
from car_rental.models.order import Orders

runner = CliRunner()


@pytest.fixture(name="rows_count", scope="module")
def count_row():
    rows_count = session.query(Cars).count()
    return rows_count


# add row on the last position
@patch("car_rental.commands.commands.enter_data")
def test_insert_row(mock_input, rows_count):
    mock_input.return_value = f"{rows_count+1},Opel,Corsa"
    result = runner.invoke(app, ["insert-row", "Cars"])
    assert result.exit_code == 0
    assert session.query(Cars)[rows_count].brand == "Opel"
    assert session.query(Cars)[rows_count].model == "Corsa"


def test_update_table(rows_count):
    result = runner.invoke(
        app, ["update-table", "Cars", f"{rows_count+1}", "model", "Insigna"]
    )
    assert result.exit_code == 0
    assert session.query(Cars)[rows_count].model == "Insigna"


def test_delete_row(rows_count):
    result = runner.invoke(app, ["delete-row", "Cars", f"{rows_count+1}"])
    assert result.exit_code == 0
    assert session.query(Cars.id).count() == rows_count


def test_show_table():
    result = runner.invoke(app, ["show-table", "Cars"])
    assert result.exit_code == 0


def test_search_in_table1():
    result = runner.invoke(app, ["search-in-table", "Cars", "brand", "Toyota"])
    assert result.exit_code == 0


def test_search_in_table2():
    result = runner.invoke(app, ["search-in-table", "Cars", "brand", "Mercedes"])
    assert "Mercedes" not in result.stdout