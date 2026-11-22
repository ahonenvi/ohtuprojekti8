# ohtuprojekti8

## Projektin dokumentit

Backlog:[Google Sheets](https://docs.google.com/spreadsheets/d/1WEF7D19tYA4jiRd3K7fiMO6fH5h0ZEb97zJawraTAos/edit?gid=1#gid=1)

## Definition of done

1. User storyjen hyväksymiskriteerit
2. Testikattavuus
3. Jatkuva integraatio (CI)
4. Koodin ylläpitäminen: arkkitehtuuri, nimeäminen, koodityyli ja dokumentaatio 

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

### lopeta

Sulkee ohjelman.