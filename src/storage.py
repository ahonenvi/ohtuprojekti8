import json
from pathlib import Path


def save_references(references, file_path):
    """Tallentaa viitteet JSON-tiedostoon."""
    file_path = Path(file_path)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(references, file, ensure_ascii=False, indent=4)


def load_references(file_path):
    """Lataa viitteet JSON-tiedostosta."""
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []