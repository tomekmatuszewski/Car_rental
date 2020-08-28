import pytest
from car_rental.control.utils import parse_data


@pytest.mark.parametrize(
    "input1,input2,result",
    (
        ("1,2,3", ["col1", "col2", "col3"], {"col1": "1", "col2": "2", "col3": "3"}),
        ("a,b,c", ["col1", "col2", "col3"], {"col1": "a", "col2": "b", "col3": "c"}),
        ("a,b,c", [1, 2, 3], {1: "a", 2: "b", 3: "c"}),
    ),
)
def test_parse_data(input1, input2, result):
    assert parse_data(input1, input2) == result
