import json
from pathlib import Path

base = Path(__file__).parent
ref_file = base / "references.json"


def save_references(references):
    """Tallentaa viitteet JSON-tiedostoon."""

    with open(ref_file, "w", encoding="utf-8") as file:
        json.dump(references, file, ensure_ascii=False, indent=4)


def load_references():
    """Lataa viitteet JSON-tiedostosta."""

    if not ref_file.exists():
        return []

    with open(ref_file, "r", encoding="utf-8") as file:
        return json.load(file)