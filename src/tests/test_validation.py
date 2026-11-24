
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from validation import validate_reference


def test_valid_reference():
    reference = {
        "type": "book",
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
        "type": "book",
        "author": "Meikäläinen, Maija",
        "title": "Kolme muskettisoturia",
        "year": year
    }

    errors = validate_reference(reference)

    assert len(errors) > 0


def test_missing_author():
    reference = {
        "type": "book",
        "author": "",
        "title": "Kolme muskettisoturia",
        "year": "2009"
    }

    errors = validate_reference(reference)

    assert len(errors) > 0


def test_missing_title():
    reference = {
        "type": "book",
        "author": "Meikäläinen, Maija",
        "title": "",
        "year": "2009"
    }

    errors = validate_reference(reference)

    assert len(errors) > 0

def test_tuntematon_tyyppi_antaa_virheen():
    reference = {
        "type": "kirja",
        "author": "Meikäläinen, Maija",
        "title": "Kolme muskettisoturia",
        "year": "2009",
    }

    errors = validate_reference(reference)

    assert "Viitetyyppi on virheellinen (book, article tai inproceedings)" in errors


def test_sallitut_tyypit_hyvaksytaan():
    for ref_type in ("book", "article", "inproceedings"):
        reference = {
            "type": ref_type,
            "author": "Meikäläinen, Maija",
            "title": "Otsikko",
            "year": "2009",
        }

        assert validate_reference(reference) == []
