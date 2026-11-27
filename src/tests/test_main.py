import os
import tempfile
import unittest

from main import App
from storage import load_references, save_references


class StubIO:
    def __init__(self, inputs=None):
        self.inputs = inputs or []
        self.outputs = []
        self.prompts = []

    def read(self, prompt=""):
        self.prompts.append(prompt)
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
    io = StubIO(["muokkaa", "EiOle99", "lopeta"])

    App(io, tmp_path / "refs.json").run()

    assert "Tuntematon komento" not in io.outputs

def sample_reference():
    return {
        "type": "book",
        "key": "Matti17",
        "author": ["Meikäläinen, Matti"],
        "title": "Vanha otsikko",
        "year": "2017",
    }


def test_muokkaus_kysyy_kentat_ja_nayttaa_nykyiset_arvot(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)
    io = StubIO(["muokkaa", "Matti17", "", "", "", "lopeta"])

    App(io, path).run()

    assert "Tekijä [Meikäläinen, Matti]: " in io.prompts
    assert "Otsikko [Vanha otsikko]: " in io.prompts
    assert "Vuosi [2017]: " in io.prompts


def test_muokkaus_tulostaa_otsikkorivin_ja_tyhjan_rivin(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)
    io = StubIO(["muokkaa", "Matti17", "", "", "", "lopeta"])

    App(io, path).run()

    assert io.outputs[:2] == ["Muokataan viitettä Matti17", ""]


def test_muokkaus_tuntemattomalla_avaimella_ilmoittaa_virheen(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)
    io = StubIO(["muokkaa", "EiOle99", "lopeta"])

    App(io, path).run()

    assert "Viitettä avaimella EiOle99 ei löytynyt" in io.outputs
    assert not any("Otsikko [" in prompt for prompt in io.prompts)


def test_ask_edits_palauttaa_vain_syotetyt_kentat(tmp_path):
    io = StubIO(["", "Uusi otsikko", ""])
    app = App(io, tmp_path / "refs.json")

    changes = app.ask_edits(sample_reference())

    assert changes == {"title": "Uusi otsikko"}

def test_muokkaus_tallentuu(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "muokkaa",
        "Matti17",
        "",
        "Uusi otsikko",
        "",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert app.references[0]["title"] == "Uusi otsikko"
    assert app.references[0]["year"] == "2017"

    saved = load_references(path)
    assert saved[0]["title"] == "Uusi otsikko"

def test_enter_sailyttaa_vanhat_arvot(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "muokkaa",
        "Matti17",
        "",
        "",
        "",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert app.references[0] == sample_reference()

def test_virheellista_muokkausta_ei_tallenneta(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "muokkaa",
        "Matti17",
        "",
        "",
        "20a9",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert app.references[0]["year"] == "2017"
    assert "Muutoksia ei tallennettu." in io.outputs

def test_poista_komento_tunnistetaan(tmp_path):
    io = StubIO(["poista", "lopeta"])

    App(io, tmp_path / "refs.json").run()

    assert "Tuntematon komento" not in io.outputs
    assert "Ei poistettavia viitteitä." in io.outputs

def test_viitteen_poisto_onnistuu(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "poista",
        "Matti17",
        "kyllä",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert len(app.references) == 0
    assert load_references(path) == []
    assert "Viite poistettu." in io.outputs

def test_viitteen_poisto_perutaan(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "poista",
        "Matti17",
        "ei",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert len(app.references) == 1
    assert app.references[0]["key"] == "Matti17"
    assert load_references(path) == [sample_reference()]
    assert "Viitettä ei poistettu." in io.outputs

def test_poisto_tuntemattomalla_avaimella(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "poista",
        "Tuntematon99",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert len(app.references) == 1
    assert "Viitettä ei löytynyt." in io.outputs

def test_poisto_tyhjasta_listasta(tmp_path):
    io = StubIO([
        "poista",
        "lopeta"
    ])

    app = App(io, tmp_path / "refs.json")
    app.run()

    assert "Ei poistettavia viitteitä." in io.outputs

def test_poistettava_viite_tulostetaan(tmp_path):
    path = tmp_path / "refs.json"
    save_references([sample_reference()], path)

    io = StubIO([
        "poista",
        "Matti17",
        "ei",
        "lopeta"
    ])

    app = App(io, path)
    app.run()

    assert "Olet poistamassa seuraavaa viitettä:" in io.outputs
    assert any("[Matti17]" in output for output in io.outputs)
    