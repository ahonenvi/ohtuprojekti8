import unittest
from main import App, format_reference


class StubIO:
    def __init__(self):
        self.outputs = []

    def write(self, value):
        self.outputs.append(value)


class TestListaus(unittest.TestCase):

    def setUp(self):
        self.io = StubIO()
        self.app = App(self.io)

    def test_tyhjien_viitteiden_listaus(self):
        self.app.list_references()

        self.assertEqual(
            self.io.outputs,
            ["Ei tallennettuja viitteitä."]
        )

    def test_yhden_viitteen_listaus(self):
        self.app.references.append({
            "type": "Kirja",
            "author": "Matti Meikäläinen",
            "title": "Python perusteet",
            "year": "2025"
        })

        self.app.list_references()

        self.assertEqual(
            self.io.outputs,
            ["Matti Meikäläinen (2025): Python perusteet [Kirja]"]
        )

    def test_usean_viitteen_listaus(self):
        self.app.references = [
            {
                "type": "Kirja",
                "author": "Matti Meikäläinen",
                "title": "Python perusteet",
                "year": "2025"
            },
            {
                "type": "Artikkeli",
                "author": "Liisa Virtanen",
                "title": "Ohjelmoinnin oppiminen",
                "year": "2024"
            }
        ]

        self.app.list_references()

        self.assertEqual(len(self.io.outputs), 2)

        self.assertEqual(
            self.io.outputs[0],
            "Matti Meikäläinen (2025): Python perusteet [Kirja]"
        )

        self.assertEqual(
            self.io.outputs[1],
            "Liisa Virtanen (2024): Ohjelmoinnin oppiminen [Artikkeli]"
        )

    def test_viitteen_muotoilu(self):
        reference = {
            "type": "Kirja",
            "author": "Matti Meikäläinen",
            "title": "Python perusteet",
            "year": "2025"
        }

        result = format_reference(reference)

        self.assertEqual(
            result,
            "Matti Meikäläinen (2025): Python perusteet [Kirja]"
        )


if __name__ == "__main__":
    unittest.main()

    
