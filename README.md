# ohtuprojekti8

## Projektin dokumentit

Backlog:[Google Sheets](https://docs.google.com/spreadsheets/d/1WEF7D19tYA4jiRd3K7fiMO6fH5h0ZEb97zJawraTAos/edit?gid=1#gid=1)

## Definition of done

1. User storyjen hyväksymiskriteerit täyttyvät
2. Testikattavuus on kohtuullinen
3. Asiakas pääsee näkemään koodin ja testien tilanteen CI-palvelusta
4. Koodin ylläpitäminen on hyvä: arkkitehtuuri, nimeäminen, koodityyli ja dokumentaatio ovat järkeviä 

## Asennus

Tarvitset uv komentorivityökalun. Lataa repositorio ja asenna riippuvuudet:

    git clone https://github.com/ahonenvi/ohtuprojekti8.git
    cd ohtuprojekti8
    uv sync

## Käynnistys

    cd src
    uv run python main.py

## Komennot

### lisaa

Lisää uuden viitteen. Ohjelma kysyy seuraavat tiedot:

- Viitteen tyyppi (esim. "kirja")
- Tekijä (muodossa "Sukunimi, Etunimi")
- Otsikko
- Julkaisuvuosi

Jos jokin tieto puuttuu tai on virheellinen, ohjelma tulostaa virheilmoituksen
eikä tallenna viitettä. Onnistuneen lisäyksen jälkeen ohjelma tulostaa
"Viite lisätty".

### listaa

Tulostaa kaikki tallennetut viitteet, yksi viite per rivi muodossa:

    Tekijä (vuosi): Otsikko [tyyppi]

Jos viitteitä ei ole, ohjelma kertoo siitä. Komento ei muuta tallennettuja viitteitä.
### lopeta

Sulkee ohjelman.

## Tallennus

Viitteet tallentuvat JSON-muodossa tiedostoon `references.json`, ja ne ladataan
automaattisesti, kun ohjelma käynnistetään. Aiemmin tallennetut viitteet säilyvät
siis uusien viitteiden lisäämisen ja ohjelman uudelleenkäynnistyksen jälkeen.

Tiedosto luodaan kansioon, josta ohjelma käynnistetään (yllä olevilla ohjeilla
`src`-kansioon). Käynnistä ohjelma aina samasta kansiosta, jotta se löytää
aiemmin tallennetut viitteet. Tiedosto on `.gitignore`ssa, eikä se kuulu repoon.

## Testit

    uv run pytest

Testit käyttävät väliaikaisia tiedostoja, eivätkä ne koske oikeaan `references.json`-tiedostoon.