import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from storage import save_references, load_references


def test_save_references(tmp_path):
    references = [
        {
            "type": "kirja",
            "author": "Meikäläinen, Maija",
            "title": "Kolme muskettisoturia",
            "year": "2009"
        }
    ]

    file_path = tmp_path / "references.json"

    save_references(references, file_path)

    assert file_path.exists()

    with open(file_path, encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == references


def test_load_references(tmp_path):
    references = [
        {
            "type": "kirja",
            "author": "Meikäläinen, Maija",
            "title": "Kolme muskettisoturia",
            "year": "2009"
        }
    ]

    file_path = tmp_path / "references.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(references, file)

    loaded_references = load_references(file_path)

    assert loaded_references == references


def test_load_references_when_file_does_not_exist(tmp_path):
    file_path = tmp_path / "missing.json"

    loaded_references = load_references(file_path)

    assert loaded_references == []
