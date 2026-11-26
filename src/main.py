
from storage import load_references, save_references
from validation import validate_reference
from keys import generate_key

DEFAULT_FILE = "references.json"


class ConsoleIO:
    def read(self, prompt=""):
        return input(prompt)

    def write(self, value):
        print(value)


class App:
    def __init__(self, io, file_path=DEFAULT_FILE):
        self.io = io
        self.file_path = file_path
        self.references = load_references(file_path)

    def run(self):
        while True:
            command = self.io.read("Komento (lisaa, listaa, poista tai lopeta): ")

            if command == "lisaa":
                self.add_reference()
            elif command == "listaa":
                self.list_references()
            elif command == "poista":
                self.remove_reference()
            elif command == "lopeta":
                break
            else:
                self.io.write("Tuntematon komento")

    def add_reference(self):
        reference = {
            "type": self.io.read("Viitteen tyyppi (book, article, inproceedings): "),
            "author": parse_authors(self.io.read("Tekijät: ")),
            "title": self.io.read("Otsikko: "),
            "year": self.io.read("Julkaisuvuosi: "),
        }

        errors = validate_reference(reference)

        if errors:
            for error in errors:
                self.io.write(error)

            self.io.write("Viitettä ei tallennettu")
            return

        existing_keys = [ref.get("key", "") for ref in self.references]
        reference["key"] = generate_key(
            reference["author"], reference["year"], existing_keys
        )

        self.references.append(reference)
        save_references(self.references, self.file_path)
        self.io.write(f"Viite lisätty, viiteavain: {reference['key']}")

    def list_references(self):

        if not self.references:
            self.io.write("Ei tallennettuja viitteitä.")
            return

        for reference in self.references:
            self.io.write(format_reference(reference))

    def remove_reference(self):
        if not self.references:
            self.io.write("Ei poistettavia viitteitä.")
            return

        key = self.io.read("Anna poistettavan viitteen avain: ")

        reference = next(
            (ref for ref in self.references if ref.get("key") == key),
            None
        )

        if reference is None:
            self.io.write("Viitettä ei löytynyt.")
            return

        self.io.write("Olet poistamassa seuraavaa viitettä:")
        self.io.write(format_reference(reference))

        confirmation = self.io.read(
            "Haluatko varmasti poistaa viitteen? (kyllä/ei): "
        ).lower()

        if confirmation == "kyllä":
            self.references.remove(reference)
            save_references(self.references, self.file_path)
            self.io.write("Viite poistettu.")
        else:
            self.io.write("Viitettä ei poistettu.")


def parse_authors(text):
    return [author.strip() for author in text.split(";") if author.strip()]

def format_reference(reference):
    """Muodostaa viitteestä yhden rivin esityksen."""

    authors = reference["author"]
    if isinstance(authors, list):
        authors = "; ".join(authors)

    key = reference.get("key", "-")
    return (
        f"[{key}] "
        f"{authors} "
        f"({reference['year']}): "
        f"{reference['title']} "
        f"[{reference['type']}]"
    )

def main():
    App(ConsoleIO()).run()


if __name__ == "__main__":
    main()

