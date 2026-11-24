
import re

ALLOWED_TYPES = ("book", "article", "inproceedings")


def validate_reference(reference):
    """Tarkistaa viitteen pakolliset tiedot."""

    errors = []

    if reference.get("type", "").strip() not in ALLOWED_TYPES:
        errors.append("Viitetyyppi on virheellinen (book, article tai inproceedings)")

    if not reference.get("author", "").strip():
        errors.append("Tekijä puuttuu")

    if not reference.get("title", "").strip():
        errors.append("Otsikko puuttuu")

    year = reference.get("year", "")

    if not re.fullmatch(r"\d{4}", year):
        errors.append("Julkaisuvuoden pitää olla nelinumeroinen")

    return errors
