
from itertools import count
from string import ascii_lowercase



def split_authors(author_field):
    """Jakaa tekijäkentän tekijöiksi. Kenttä on lista tai merkkijono (erottimet: ; tai ' and ')."""
    if isinstance(author_field, list):
        return [author.strip() for author in author_field if author.strip()]

    parts = author_field.replace(" and ", ";").split(";")
    return [part.strip() for part in parts if part.strip()]


def name_parts(author):
    """Palauttaa (sukunimi, etunimi). Hyväksyy muodot 'Sukunimi, Etunimi' ja 'Sukunimi Etunimi'."""
    if "," in author:
        surname, first = author.split(",", 1)
    else:
        tokens = author.split()
        surname, first = tokens[0], " ".join(tokens[1:])
    return surname.strip(), first.strip()


def _base_key(author_field, year):
    authors = split_authors(author_field)

    if len(authors) == 1:
        surname, first = name_parts(authors[0])
        name = first.split()[0] if first else surname
        return name + year[-2:]                   # Matti17

    initials = "".join(name_parts(a)[0][:1] for a in authors)
    return initials + year[-2:]                   # MN20


def _candidates(base):
    yield base
    for letter in ascii_lowercase:
        yield base + letter
    for number in count(1):
        yield f"{base}{number}"


def generate_key(author_field, year, existing_keys=()):
    """Luo uniikin viiteavaimen tekijöistä ja vuodesta."""
    base = _base_key(author_field, year) or f"viite{year}"
    used = {key.lower() for key in existing_keys}

    for candidate in _candidates(base):
        if candidate.lower() not in used:
            return candidate