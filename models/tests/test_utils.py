from models.utils import *
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    (
        ("tm@o2.pl", True),
        ("tmo2.pl", False),
        ("john_noval_pl@gmail.com", True),
        ("dnsndksd", False),
    ),
)
def test_email_validator(test_input, expected):
    assert email_validator(test_input) == expected
