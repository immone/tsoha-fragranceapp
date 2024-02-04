# tsoha-fragranceapp
Sovelluksen avulla voi listata eri hajuvesiä sekä keskustella ja arvostella niitä.

Sovelluksen ominaisuuksia ovat:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä näkee etusivulla listan viimeisimmin kommentoiduista hajuvesistä.
* Käyttäjä voi hakea sovelluksessa hajuvesiä sekä tutkia kutakin hajuvettä sen oman sivuston kautta.
* Käyttäjä voi lisätä profiiliinsa tiedon siitä, että omistaa kyseisen hajuveden.
* Käyttäjä voi arvostella hajuveden (liukuvalla asteikolla 1-10) ja jättää siihen kommentin.
* Käyttäjä voi tutkia suosituimpia hajuvesiä tilastoista.
* Ylläpitäjä voi lisätä tai poistaa hajuveden.
* Ylläpitäjä voi poistaa tarvittaessa käyttäjän arvion.
* Ylläpitäjä voi luokitella hajuvesiä eri joukkoihin niiden ominaisuuksien mukaan.


## Dokumentaatio
[Vaatimusmäärittely](https://github.com/immone/tsoha-fragranceapp/blob/main/documentation/vaatimusmaarittely.md)

[Tuntikirjanpito](https://github.com/immone/tsoha-fragranceapp/blob/main/documentation/tuntikirjanpito.md)

[Selvitys tekoälyn käytöstä](https://github.com/immone/tsoha-fragranceapp/blob/main/documentation/tekoalyn_kaytto.md)

## Asennus

1. Luo virtuaaliympäristö komennolla `python3 -m venv venv`
2. Käynnistä virtuaaliympäristö komennolla `source venv/bin/activate`
3. Asenna ohjelmiston riippuvuudet komennolla ` pip install -r requirements.txt`
4. Luo sovelluksen tarvitsema [PostgreSQL-skeema](https://github.com/immone/tsoha-fragranceapp/blob/main/data/schema.sql)
5. Käynnistä sovellus paikallisesti komennolla `flask run`
