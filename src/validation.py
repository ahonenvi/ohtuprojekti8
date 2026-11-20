
import re


def validate_reference(reference):
    """Tarkistaa viitteen pakolliset tiedot."""

    errors = []

    if not reference.get("author", "").strip():
        errors.append("Tekijä puuttuu")

    if not reference.get("title", "").strip():
        errors.append("Otsikko puuttuu")

    year = reference.get("year", "")

    if not re.fullmatch(r"\d{4}", year):
        errors.append("Julkaisuvuoden pitää olla nelinumeroinen")

    return errors
