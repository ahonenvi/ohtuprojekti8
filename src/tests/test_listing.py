import os
import tempfile
import unittest

from main import App, format_reference


class StubIO:
    def __init__(self):
        self.outputs = []

    def write(self, value):
        self.outputs.append(value)


class TestListaus(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.io = StubIO()
        self.app = App(self.io, os.path.join(self.tmp.name, "refs.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_tyhjien_viitteiden_listaus(self):
        self.app.list_references()

        self.assertEqual(
            self.io.outputs,
            ["Ei tallennettuja viitteitä."]
        )

    def test_yhden_viitteen_listaus(self):
        self.app.references.append({
            "type": "book",
            "key": "Matti25",
            "author": "Matti Meikäläinen",
            "title": "Python perusteet",
            "year": "2025"
        })

        self.app.list_references()

        self.assertEqual(
            self.io.outputs,
            ["[Matti25] Matti Meikäläinen (2025): Python perusteet [book]"]
        )

    def test_usean_viitteen_listaus(self):
        self.app.references = [
            {
                "type": "book",
                "key": "Matti25",
                "author": "Matti Meikäläinen",
                "title": "Python perusteet",
                "year": "2025"
            },
            {
                "type": "article",
                "key": "Liisa24",
                "author": "Liisa Virtanen",
                "title": "Ohjelmoinnin oppiminen",
                "year": "2024"
            }
        ]

        self.app.list_references()

        self.assertEqual(len(self.io.outputs), 2)

        self.assertEqual(
            self.io.outputs[0],
            "[Liisa24] Liisa Virtanen (2024): Ohjelmoinnin oppiminen [article]"
        )

        self.assertEqual(
            self.io.outputs[1],
            "[Matti25] Matti Meikäläinen (2025): Python perusteet [book]"
        )

    def test_viitteen_muotoilu(self):
        reference = {
            "type": "book",
            "key": "Matti25",
            "author": "Matti Meikäläinen",
            "title": "Python perusteet",
            "year": "2025"
        }

        result = format_reference(reference)

        self.assertEqual(
            result,
            "[Matti25] Matti Meikäläinen (2025): Python perusteet [book]"
        )

    def test_useita_tekijoita_listauksessa(self):
        reference = {
            "type": "book",
            "key": "MV25",
            "author": ["Meikäläinen, Maija", "Virtanen, Liisa"],
            "title": "Python perusteet",
            "year": "2025"
        }

        self.assertEqual(
            format_reference(reference),
            "[MV25] Meikäläinen, Maija; Virtanen, Liisa (2025): Python perusteet [book]"
        )

    def test_listaus_on_aakkosjarjestyksessa(self):
        self.app.references = [
            {"type": "book", "key": "Z25", "author": ["Öhman, Olli"],
             "title": "Kolmas", "year": "2025"},
            {"type": "book", "key": "A25", "author": ["Aalto, Aino"],
             "title": "Ensimmäinen", "year": "2025"},
            {"type": "book", "key": "M25", "author": ["Mäki, Matti"],
             "title": "Toinen", "year": "2025"},
        ]

        self.app.list_references()

        self.assertEqual(
            self.io.outputs,
            [
                "[A25] Aalto, Aino (2025): Ensimmäinen [book]",
                "[M25] Mäki, Matti (2025): Toinen [book]",
                "[Z25] Öhman, Olli (2025): Kolmas [book]",
            ],
        )

    def test_listaus_ei_muuta_jarjestysta_muistissa(self):
        self.app.references = [
            {"type": "book", "key": "B", "author": ["B"], "title": "t", "year": "2025"},
            {"type": "book", "key": "A", "author": ["A"], "title": "t", "year": "2025"},
        ]

        self.app.list_references()

        self.assertEqual([r["key"] for r in self.app.references], ["B", "A"])


if __name__ == "__main__":
    unittest.main()