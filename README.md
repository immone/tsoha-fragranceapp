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
3. Asenna ohjelmiston riippuvuudet komennolla `pip install -r requirements.txt`
4. Luo sovelluksen tarvitsema [PostgreSQL-skeema](https://github.com/immone/tsoha-fragranceapp/blob/main/data/schema.sql)
5. Luo tiedoston juureen `.env` tiedosto, jossa on tarvittavat arvot seuraaville muuttujille:
```
DATABASE_URL=
SECRET_KEY=
FLASK_APP=app.py
UPLOAD_PATH=static/images
```
Tässä `DATABASE_URL` on viittaus  PostgreSQL-tietokantaan, joka on muotoa `postgresql:///xxx` ja `SECRET_KEY` istuntojen salaukseen tarvittava 32-bittinen avain (luo esimerkiksi Pythonin `secrets`-kirjaston avulla komennolla `secrets.token_hex(16)`)

6. Käynnistä sovellus paikallisesti komennolla `flask run`

## Käyttöesimerkki

Kun olet käynnistänyt ohjelman paikallisesti, avaa selain ja kirjoita siihen osoite `http://127.0.0.1:5000`. Saat lisättyä tietokantaan uusia hajuvesiä ensin luomalla uuden käyttäjätunnuksen (`Log in` -> `Register here`), jonka jälkeen oikealla olevasta paneelista `Headuser panel` pääset lisäämään tietokantaan uuden hajuveden painamalla nappia `Add a new fragrance`.
