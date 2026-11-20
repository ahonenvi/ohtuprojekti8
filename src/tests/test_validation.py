
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from validation import validate_reference


def test_valid_reference():
    reference = {
        "type": "kirja",
        "author": "Meikäläinen, Maija",
        "title": "Kolme muskettisoturia",
        "year": "2009"
    }

    assert validate_reference(reference) == []


@pytest.mark.parametrize("year", [
    "09",
    "200",
    "20099",
    "20a9",
    ""
])
def test_invalid_year(year):
    reference = {
        "type": "kirja",
        "author": "Meikäläinen, Maija",
        "title": "Kolme muskettisoturia",
        "year": year
    }

    errors = validate_reference(reference)

    assert len(errors) > 0


def test_missing_author():
    reference = {
        "type": "kirja",
        "author": "",
        "title": "Kolme muskettisoturia",
        "year": "2009"
    }

    errors = validate_reference(reference)

    assert len(errors) > 0


def test_missing_title():
    reference = {
        "type": "kirja",
        "author": "Meikäläinen, Maija",
        "title": "",
        "year": "2009"
    }

    errors = validate_reference(reference)

    assert len(errors) > 0
