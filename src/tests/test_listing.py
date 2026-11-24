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
            "author": "Matti Meikäläinen",
            "title": "Python perusteet",
            "year": "2025"
        })

        self.app.list_references()

        self.assertEqual(
            self.io.outputs,
            ["Matti Meikäläinen (2025): Python perusteet [book]"]
        )

    def test_usean_viitteen_listaus(self):
        self.app.references = [
            {
                "type": "book",
                "author": "Matti Meikäläinen",
                "title": "Python perusteet",
                "year": "2025"
            },
            {
                "type": "article",
                "author": "Liisa Virtanen",
                "title": "Ohjelmoinnin oppiminen",
                "year": "2024"
            }
        ]

        self.app.list_references()

        self.assertEqual(len(self.io.outputs), 2)

        self.assertEqual(
            self.io.outputs[0],
            "Matti Meikäläinen (2025): Python perusteet [book]"
        )

        self.assertEqual(
            self.io.outputs[1],
            "Liisa Virtanen (2024): Ohjelmoinnin oppiminen [article]"
        )

    def test_viitteen_muotoilu(self):
        reference = {
            "type": "book",
            "author": "Matti Meikäläinen",
            "title": "Python perusteet",
            "year": "2025"
        }

        result = format_reference(reference)

        self.assertEqual(
            result,
            "Matti Meikäläinen (2025): Python perusteet [book]"
        )

    def test_useita_tekijoita_listauksessa(self):
        reference = {
            "type": "book",
            "author": ["Meikäläinen, Maija", "Virtanen, Liisa"],
            "title": "Python perusteet",
            "year": "2025"
        }

        self.assertEqual(
            format_reference(reference),
            "Meikäläinen, Maija; Virtanen, Liisa (2025): Python perusteet [book]"
        )


if __name__ == "__main__":
    unittest.main()