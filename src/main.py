class ConsoleIO:
    def read(self, prompt=""):
        return input(prompt)

    def write(self, value):
        print(value)

class App:
    def __init__(self,io):
        self.io = io
        self.references = []

    def run(self):
        while True:
            command = self.io.read("Komento (lisaa tai lopeta): ")
            if command == "lisaa":
                self.add_reference()
            elif command == "lopeta":
                break
            else:
                self.io.write("Tuntematon komento")

    def add_reference(self):
        reference = {
            "type": self.io.read("Viitteen tyyppi: "),
            "author": self.io.read("Tekijä: "),
            "title": self.io.read("Otsikko: "),
            "year": self.io.read("Julkaisuvuosi: "),
        }
        self.references.append(reference)
        self.io.write("Viite lisätty")

def main():
    App(ConsoleIO()).run()

if __name__ == "__main__":
    main()