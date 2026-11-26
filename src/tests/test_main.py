import os
import tempfile
import unittest

from main import App


class StubIO:
    def __init__(self, inputs=None):
        self.inputs = inputs or []
        self.outputs = []

    def read(self, prompt=""):
        return self.inputs.pop(0)

    def write(self, value):
        self.outputs.append(value)


class TestLisaaKomento(unittest.TestCase):
    def test_lisaa_kysyy_tiedot(self):
        io = StubIO([
            "lisaa",
            "book",
            "Meikäläinen, Maija",
            "Kolme muskettisoturia",
            "2009",
            "lopeta"
        ])

        with tempfile.TemporaryDirectory() as tmp:
            app = App(io, os.path.join(tmp, "refs.json"))
            app.run()

        self.assertEqual(len(app.references), 1)
        self.assertEqual(app.references[0]["type"], "book")
        self.assertEqual(app.references[0]["author"], ["Meikäläinen, Maija"])
        self.assertEqual(app.references[0]["title"], "Kolme muskettisoturia")
        self.assertEqual(app.references[0]["year"], "2009")


def test_useita_tekijoita(tmp_path):
    io = StubIO([
            "lisaa",
            "book",
            "Meikäläinen, Maija; Ankka, Aku",
            "Kolme muskettisoturia",
            "2009",
            "lopeta"
        ])

    app = App(io, tmp_path / "refs.json")
    app.run()
    
    assert app.references[0]["author"] == [
        "Meikäläinen, Maija",
        "Ankka, Aku"
    ]
    

def test_virheellista_viitetta_ei_lisata(tmp_path):
    io = StubIO([
        "lisaa",
        "book",
        "Meikäläinen, Maija",
        "Kolme muskettisoturia",
        "20a9",
        "lopeta"
    ])

    app = App(io, tmp_path / "refs.json")
    app.run()

    assert len(app.references) == 0
    assert "Viitettä ei tallennettu" in io.outputs

def test_tuntematon_tyyppi_ei_tallennu(tmp_path):
    io = StubIO([
        "lisaa",
        "kirja",
        "Meikäläinen, Maija",
        "Kolme muskettisoturia",
        "2009",
        "lopeta"
    ])

    app = App(io, tmp_path / "refs.json")
    app.run()

    assert len(app.references) == 0
    assert "Viitettä ei tallennettu" in io.outputs

def test_muokkaa_komento_tunnistetaan(tmp_path):
    io = StubIO(["muokkaa", "lopeta"])

    App(io, tmp_path / "refs.json").run()

    assert "Tuntematon komento" not in io.outputs
    