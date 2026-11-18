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
        io = StubIO(["lisaa", "kirja", "Meikäläinen, Maija", "Kolme muskettisoturia", 
                     "2009", "lopeta"])

        app = App(io)
        app.run()

        self.assertEqual(len(app.references), 1)
        self.assertEqual(app.references[0]["type"], "kirja")
        self.assertEqual(app.references[0]["author"], "Meikäläinen, Maija")
        self.assertEqual(app.references[0]["title"], "Kolme muskettisoturia")
        self.assertEqual(app.references[0]["year"], "2009")    