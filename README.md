# Viešbučio valdymo sistema

## Kursinio darbo ataskaita

---

## 1. Įvadas

Mano kursinio darbo tikslas buvo sukurti programinę sistemą, kurioje būtų praktiškai pritaikyti objektinio programavimo principai, projektavimo šablonai, kompozicijos ir agregacijos ryšiai, taip pat įgyvendintas darbas su failais bei programos testavimas.

Mano pasirinkta tema yra viešbučio valdymo sistema. Ją pasirinkau todėl, kad tokioje sistemoje egzistuoja keli tarpusavyje susiję objektai, tokie kaip kambariai, svečiai, rezervacijos ir pats viešbutis. Kiekvienas iš šių elementų turi savitas savybes ir funkcijas, todėl juos patogu reprezentuoti naudojant atskiras klases, o tai leidžia aiškiai pritaikyti objektinio programavimo principus.

Mano sukurta valdymo sistema programa leidžia vartotojui:

- peržiūrėti visus viešbučio kambarius;
- peržiūrėti tik laisvus kambarius;
- pridėti naują kambarį;
- pridėti naują svečią;
- sukurti rezervaciją;
- atlikti svečio **check-in**;
- atlikti svečio **check-out**;
- atšaukti rezervaciją;
- apskaičiuoti bendras viešbučio pajamas;
- išsaugoti ir įkelti duomenis iš JSON failo.

Programa parašyta **Python** programavimo kalba ir veikia per tekstinę vartotojo sąsają, t. y. komandinėje eilutėje. Vartotojas pasirenka norimą veiksmą iš meniu, o programa atlieka pasirinktą operaciją.

### Programos paleidimas

```bash
python hotel_system.py
```

### Testų paleidimas

```bash
python -m unittest test_hotel_system.py
```

Programa yra paprasta naudoti: paleidus failą, vartotojui parodomas meniu su numeruotomis parinktimis. Vartotojas įveda pasirinkimo numerį ir toliau įveda reikalingus duomenis, pavyzdžiui, svečio vardą, pavardę, telefono numerį, el. paštą, kambario numerį ar nakvynių skaičių.

---

## 2. Sistemos analizė ir struktūra

Sistema sudaryta iš kelių pagrindinių klasių:

- `Guest` – saugo svečio informaciją;
- `Room` – abstrakti bazinė kambario klasė;
- `StandardRoom` – standartinio kambario klasė;
- `DeluxeRoom` – geresnio kambario klasė;
- `SuiteRoom` – liukso kambario klasė;
- `Reservation` – rezervacijos klasė;
- `Hotel` – pagrindinė viešbučio valdymo klasė;
- `RoomFactory` – kambarių kūrimo klasė;
- `FileManager` – duomenų išsaugojimo ir įkėlimo klasė.

Tokia struktūra pasirinkta todėl, kad kiekviena klasė turi aiškią atsakomybę. Pavyzdžiui, `Guest` klasė atsakinga tik už svečio duomenis, `Room` ir jos paveldėtos klasės – už kambarių informaciją ir kainos skaičiavimą, `Reservation` – už rezervacijos būseną, o `Hotel` – už bendrą sistemos valdymą.

Toks atsakomybių atskyrimas padaro kodą aiškesnį, lengviau skaitomą, lengviau testuojamą ir paprasčiau plečiamą ateityje.

---

## 3. Objektinio programavimo principai

Šiame projekte panaudoti visi keturi pagrindiniai objektinio programavimo principai:

- inkapsuliacija;
- paveldėjimas;
- abstrakcija;
- polimorfizmas.

---

### 3.1 Enkapsuliacija

Enkapsuliacija reiškia, kad duomenys ir veiksmai su tais duomenimis yra laikomi vienoje klasėje. Tai leidžia valdyti objekto būseną per metodus, o ne tiesiogiai keisti duomenis bet kurioje programos vietoje.

Šiame projekte enkapsuliacija matoma keliose vietose. Pavyzdžiui, `Room` klasėje kambario užimtumo būsena keičiama naudojant `book()` ir `release()` metodus.

```python
def book(self):
    if not self.available:
        raise ValueError("Room is not available.")
    self.available = False
```

Šis metodas ne tik pakeičia kambario būseną, bet ir patikrina, ar kambarys tikrai yra laisvas. Tai apsaugo programą nuo neteisingo veiksmo, kai bandoma rezervuoti jau užimtą kambarį.

Kitas pavyzdys yra `Hotel` klasė. Joje kambariai, svečiai ir rezervacijos saugomi atskiruose sąrašuose:

```python
self._rooms = []
self._guests = []
self._reservations = []
```

Šie sąrašai priklauso `Hotel` objektui, todėl visa viešbučio informacija yra valdoma vienoje vietoje. Tai padeda išlaikyti tvarkingą programos struktūrą.

---

### 3.2 Paveldėjimas

Paveldėjimas leidžia sukurti bendrą bazinę klasę ir iš jos išvesti konkretesnes klases. Tai sumažina kodo dubliavimą, nes bendri atributai ir metodai aprašomi vienoje vietoje.

Šiame projekte paveldėjimas naudojamas kambarių klasėse. Bazinė klasė yra `Room`, o ją paveldi:

- `StandardRoom`;
- `DeluxeRoom`;
- `SuiteRoom`.

Pavyzdys:

```python
class StandardRoom(Room):
    def calculate_price(self, nights):
        return self.price * nights
```

Visi kambarių tipai turi bendrus atributus:

- kambario numerį;
- kainą;
- užimtumo būseną.

Šie bendri duomenys aprašyti bazinėje `Room` klasėje. Konkretūs kambarių tipai paveldi šiuos duomenis ir tik pakeičia kainos skaičiavimo logiką.

Toks sprendimas yra naudingas, nes jei reikėtų pridėti naują kambario tipą, pavyzdžiui, `FamilyRoom` arba `EconomyRoom`, būtų galima sukurti naują klasę, kuri paveldi `Room`, ir aprašyti tik jai būdingą kainos skaičiavimą.

---

### 3.3 Abstrakcija

Abstrakcija reiškia, kad programa aprašo bendrą objekto struktūrą, bet paslepia konkrečias realizacijos detales. Šiame projekte abstrakcija realizuota naudojant `ABC` ir `abstractmethod`.

`Room` klasė yra abstrakti:

```python
class Room(ABC):
    @abstractmethod
    def calculate_price(self, nights):
        raise NotImplementedError

    @abstractmethod
    def room_type(self):
        raise NotImplementedError
```

Tai reiškia, kad `Room` klasė nurodo, kokius metodus privalo turėti visi kambarių tipai. Kiekvienas konkretus kambarys turi turėti metodus `calculate_price()` ir `room_type()`.

Abstrakcija naudinga todėl, kad programa gali dirbti su bendru `Room` tipu, nežinodama konkrečios klasės. Tai leidžia išlaikyti aiškią struktūrą ir užtikrina, kad visi kambarių tipai turės vienodą sąsają.

---

### 3.4 Polimorfizmas

Polimorfizmas reiškia, kad skirtingi objektai gali turėti tą patį metodą, tačiau tas metodas gali veikti skirtingai.

Šiame projekte polimorfizmas naudojamas kainos skaičiavime. Visi kambarių tipai turi metodą `calculate_price()`, bet kiekvienas jį realizuoja kitaip.

`StandardRoom`:

```python
class StandardRoom(Room):
    def calculate_price(self, nights):
        return self.price * nights
```

`DeluxeRoom`:

```python
class DeluxeRoom(Room):
    def calculate_price(self, nights):
        return self.price * 1.3 * nights
```

`SuiteRoom`:

```python
class SuiteRoom(Room):
    def calculate_price(self, nights):
        return self.price * 1.6 * nights
```

`Reservation` klasė naudoja šį metodą taip:

```python
def total(self):
    return self.room.calculate_price(self.nights)
```

Svarbu tai, kad `Reservation` klasei nereikia žinoti, koks tiksliai yra kambario tipas. Ji tiesiog kviečia `calculate_price()`, o Python automatiškai panaudoja tinkamą metodą pagal objekto tipą.

Tai yra aiškus polimorfizmo pavyzdys, nes tas pats metodas skirtinguose objektuose veikia skirtingai.

---

## 4. Dizaino šablonas

Šiame projekte naudojamas **Factory Method** dizaino šablonas. Jis realizuotas `RoomFactory` klasėje.

```python
class RoomFactory:
    @staticmethod
    def create(room_type, number, price):
        room_type = room_type.lower()

        if room_type == "standard":
            return StandardRoom(number, price)
        if room_type == "deluxe":
            return DeluxeRoom(number, price)
        if room_type == "suite":
            return SuiteRoom(number, price)

        raise ValueError("Invalid room type. Use standard, deluxe, or suite.")
```

Factory Method šablonas pasirinktas todėl, kad sistemoje yra keli skirtingi kambarių tipai. Vietoje to, kad skirtingose programos vietose būtų tiesiogiai kuriami `StandardRoom`, `DeluxeRoom` ar `SuiteRoom` objektai, visa kambarių kūrimo logika sutelkta vienoje klasėje.

Šio sprendimo privalumai:

- kambarių kūrimo logika yra vienoje vietoje;
- kodas tampa tvarkingesnis;
- lengviau pridėti naują kambario tipą;
- sumažėja pasikartojančio kodo;
- pagrindinė viešbučio logika mažiau priklauso nuo konkrečių klasių.

Pavyzdžiui, jeigu ateityje reikėtų pridėti naują kambario tipą `FamilyRoom`, reikėtų sukurti naują klasę ir papildyti `RoomFactory` metodą. Kitų programos dalių keisti reikėtų mažiau.

### Kodėl pasirinktas būtent Factory Method?

`Singleton` šablonas šiam projektui netinka, nes sistemoje reikia kurti daug skirtingų objektų: daug kambarių, svečių ir rezervacijų. Singleton labiau tinka tada, kai reikia tik vieno bendro objekto.

`Builder` šablonas šiam projektui būtų per sudėtingas, nes kambario objektai nėra labai sudėtingi ir neturi daug kūrimo žingsnių.

Todėl Factory Method yra tinkamiausias pasirinkimas, nes jis paprastas, aiškus ir tiesiogiai tinka objektų kūrimui pagal tipą.

---

## 5. Kompozicija ir agregacija

Projekte naudojami kompozicijos ir agregacijos principai.

Kompozicija matoma `Hotel` klasėje. `Hotel` objektas turi sąrašus, kuriuose saugomi kambariai, svečiai ir rezervacijos:

```python
self._rooms = []
self._guests = []
self._reservations = []
```

`Hotel` klasė yra pagrindinis sistemos valdymo centras. Ji atsakinga už kambarių pridėjimą, svečių pridėjimą, rezervacijų kūrimą, paiešką ir būsenų keitimą. Tai reiškia, kad viešbutis valdo šiuos duomenis sistemos viduje.

Agregacija matoma `Reservation` klasėje. `Reservation` turi nuorodas į `Guest` ir `Room` objektus:

```python
self.guest = guest
self.room = room
```

Rezervacija susieja svečią su kambariu, tačiau svečias ir kambarys gali egzistuoti ir nepriklausomai nuo konkrečios rezervacijos. Pavyzdžiui, svečias gali būti užregistruotas sistemoje, bet dar neturėti aktyvios rezervacijos. Kambarys taip pat gali egzistuoti be rezervacijos.

---

## 6. Darbas su failais

Programa naudoja JSON failą `hotel_data.json` duomenims saugoti.

Naudojama `FileManager` klasė, kuri turi du pagrindinius metodus:

- `save_data()`;
- `load_data()`.

Duomenų išsaugojimo pavyzdys:

```python
with open(filename, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

Duomenų įkėlimo pavyzdys:

```python
with open(filename, "r", encoding="utf-8") as file:
    data = json.load(file)
```

JSON faile saugomi:

- kambariai;
- svečiai;
- rezervacijos.

JSON formatas pasirinktas todėl, kad jis yra aiškus, lengvai skaitomas ir patogus struktūriniams duomenims saugoti. Be to, Python turi integruotą `json` modulį, todėl nereikia papildomų bibliotekų.

Failų naudojimas leidžia išsaugoti programos būseną. Tai reiškia, kad uždarius programą duomenys neprarandami ir gali būti įkelti kitą kartą paleidus sistemą.

---

## 7. Klaidų valdymas ir validacija

Programa turi įvesties tikrinimą, kad vartotojas negalėtų įvesti neteisingų duomenų.

`Guest` klasėje tikrinama, ar vardas ir pavardė nėra tušti:

```python
if not name.strip() or not surname.strip():
    raise ValueError("Name and surname cannot be empty.")
```

Taip pat tikrinama, ar svečio ID yra teigiamas:

```python
if guest_id <= 0:
    raise ValueError("Guest ID must be positive.")
```

Telefono numeris turi būti lietuviško formato:

```python
if not re.fullmatch(r"\+370\d{8}", phone):
    raise ValueError("Phone must be in format +370XXXXXXXX.")
```

El. paštas taip pat tikrinamas:

```python
if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
    raise ValueError("Invalid email format.")
```

`Room` klasėje tikrinama:

- ar kambario numeris yra teigiamas;
- ar kaina nėra neigiama.

`Hotel` klasėje tikrinama:

- ar nėra dviejų kambarių su tuo pačiu numeriu;
- ar nėra dviejų svečių su tuo pačiu ID;
- ar svečias egzistuoja prieš kuriant rezervaciją;
- ar kambarys egzistuoja prieš kuriant rezervaciją;
- ar kambarys yra laisvas.

`Reservation` klasėje tikrinama:

- ar rezervacijos ID yra teigiamas;
- ar nakvynių skaičius didesnis už nulį;
- ar negalima atlikti check-in atšauktai rezervacijai;
- ar negalima atlikti check-out prieš check-in;
- ar negalima atšaukti jau užbaigtos rezervacijos.

Toks klaidų valdymas padidina programos patikimumą ir padeda išvengti neteisingų būsenų.

---

## 8. Rezervacijų būsenų valdymas

Rezervacija gali turėti kelias būsenas:

- `Reserved`;
- `Checked-in`;
- `Checked-out`;
- `Cancelled`.

`Reservation` klasėje tam naudojami trys loginiai atributai:

```python
self.checked_in = False
self.checked_out = False
self.is_cancelled = False
```

Metodas `status()` grąžina dabartinę rezervacijos būseną:

```python
def status(self):
    if self.is_cancelled:
        return "Cancelled"
    if self.checked_out:
        return "Checked-out"
    if self.checked_in:
        return "Checked-in"
    return "Reserved"
```

Tokia sistema leidžia aiškiai suprasti, kokioje būsenoje yra rezervacija. Pavyzdžiui, naujai sukurta rezervacija yra `Reserved`. Po check-in ji tampa `Checked-in`, po check-out – `Checked-out`, o atšaukus – `Cancelled`.

Tai svarbu, nes programa turi neleisti logiškai neteisingų veiksmų. Pavyzdžiui:

- negalima išregistruoti svečio, kuris dar nebuvo įregistruotas;
- negalima atšaukti jau užbaigtos rezervacijos;
- negalima įregistruoti atšauktos rezervacijos.

---

## 9. Pajamų skaičiavimas

Viešbučio pajamos skaičiuojamos `Hotel` klasėje naudojant `total_revenue()` metodą:

```python
def total_revenue(self):
    return sum(
        reservation.total()
        for reservation in self.reservations
        if reservation.checked_out and not reservation.is_cancelled
    )
```

Pajamos skaičiuojamos tik iš tų rezervacijų, kurios yra užbaigtos, t. y. svečias atliko check-out, o rezervacija nėra atšaukta.

Tai yra logiškas sprendimas, nes tik užbaigtos viešnagės laikomos realiai gautomis pajamomis. Atšauktos arba dar nebaigtos rezervacijos nėra įtraukiamos į bendras pajamas.

---

## 10. Testavimas

Programos testavimui naudojamas `unittest` frameworkas. Testai parašyti atskirame faile `test_hotel_system.py`.

Testai tikrina pagrindinę programos logiką:

- ar `RoomFactory` sukuria tinkamą kambario tipą;
- ar teisingai skaičiuojama standartinio kambario kaina;
- ar neteisingas telefono numeris sukelia klaidą;
- ar veikia rezervacijos sukūrimas;
- ar veikia check-in;
- ar veikia check-out;
- ar teisingai skaičiuojamos pajamos;
- ar neteisingas kambario tipas sukelia klaidą;
- ar galima atšaukti rezervaciją;
- ar neleidžiama pridėti svečių su tuo pačiu ID;
- ar neleidžiama pridėti kambarių su tuo pačiu numeriu.

Testo pavyzdys:

```python
def test_total_revenue_after_checkout(self):
    hotel = Hotel("Test Hotel")
    hotel.add_room(RoomFactory.create("standard", 101, 50))
    guest = Guest("Jonas", "Jonaitis", "+37061234567", 1, "jonas@email.com")
    hotel.add_guest(guest)

    reservation = hotel.create_reservation(1, 101, 2)
    hotel.check_in_guest(reservation.reservation_id)
    hotel.check_out_guest(reservation.reservation_id)

    self.assertEqual(hotel.total_revenue(), 100)
```

Šis testas patikrina, ar viešbučio pajamos skaičiuojamos teisingai po sėkmingo check-in ir check-out proceso.

Testavimas yra svarbus, nes padeda įsitikinti, kad pakeitus kodą pagrindinės funkcijos vis dar veikia teisingai.

---

## 11. Kodo stilius

Programa parašyta Python kalba ir laikosi pagrindinių PEP8 stiliaus principų.

Kode naudojami:

- aiškūs klasių pavadinimai;
- aiškūs metodų pavadinimai;
- `snake_case` stiliaus funkcijų ir kintamųjų pavadinimai;
- `CamelCase` stiliaus klasių pavadinimai;
- išimtys `ValueError` klaidų valdymui;
- aiškiai atskirtos klasės ir funkcijos.

Pavyzdžiai:

- `RoomFactory`;
- `StandardRoom`;
- `create_reservation`;
- `check_in_guest`;
- `total_revenue`.

Toks stilius padaro kodą lengviau suprantamą ir prižiūrimą.

---

## 12. Rezultatai

Darbo metu buvo sukurta veikianti viešbučio valdymo sistema, kuri leidžia atlikti pagrindinius viešbučio administravimo veiksmus.

Pagrindiniai rezultatai:

- sukurta programa, leidžianti valdyti kambarius, svečius ir rezervacijas;
- įgyvendinti visi keturi objektinio programavimo principai: inkapsuliacija, paveldėjimas, abstrakcija ir polimorfizmas;
- panaudotas Factory Method dizaino šablonas kambarių kūrimui;
- pritaikyta kompozicija ir agregacija;
- realizuotas duomenų išsaugojimas ir įkėlimas iš JSON failo;
- parašyti unit testai pagrindinei programos logikai patikrinti;
- įgyvendinta validacija ir klaidų valdymas.

Didžiausias iššūkis buvo teisingai suvaldyti rezervacijų būsenas. Reikėjo užtikrinti, kad vartotojas negalėtų atlikti logiškai neteisingų veiksmų, pavyzdžiui, atlikti check-out prieš check-in arba atšaukti jau užbaigtą rezervaciją.

---

## 13. Išvados

Atlikusi šį kursinį darbą sukūriau paprastą, bet funkcionalią viešbučio valdymo sistemą. Projektas padėjo geriau suprasti, kaip objektinio programavimo principai taikomi realioje programoje.

Darbas parodė, kad naudojant klases galima patogiai suskirstyti programą į mažesnes, aiškias dalis. Kiekviena klasė turi savo atsakomybę, todėl programą lengviau skaityti, testuoti ir tobulinti.

Enkapsuliacija padėjo apsaugoti duomenis ir valdyti objektų būsenas per metodus. Paveldėjimas leido sukurti bendrą kambarių struktūrą. Abstrakcija užtikrino, kad visi kambarių tipai turėtų reikalingus metodus. Polimorfizmas leido skirtingiems kambarių tipams skirtingai skaičiuoti kainą naudojant tą patį metodo pavadinimą.

Factory Method dizaino šablonas buvo naudingas, nes centralizavo kambarių objektų kūrimą. Tai padarė kodą tvarkingesnį ir lengviau plečiamą.

Galutinis rezultatas atitinka kursinio darbo reikalavimus: programa naudoja OOP principus, dizaino šabloną, kompoziciją ir agregaciją, failų skaitymą bei rašymą, taip pat turi unit testus.

---

## 14. Galimos plėtros kryptys

Galimi mano programos patobulinimai:

- pridėti daugiau kambarių tipų, pavyzdžiui, `EconomyRoom` arba `FamilyRoom`;
- pridėti galimybę redaguoti svečio telefono numerį arba el. paštą;
- pridėti galimybę ištrinti svečią, jeigu jis neturi aktyvių rezervacijų;
- pridėti paprastą svečio paiešką pagal vardą, pavardę arba ID;
- pridėti kambario paiešką pagal kambario numerį;
- pridėti atvykimo ir išvykimo datas rezervacijoms;
- pagerinti meniu tekstus, kad vartotojui būtų dar aiškiau, ką pasirinkti;
- pridėti daugiau testų klaidų atvejams;
- išsaugoti papildomą informaciją JSON faile, pavyzdžiui, rezervacijos sukūrimo datą;
- pridėti galimybę parodyti tik aktyvias rezervacijas;
- pridėti galimybę parodyti tik atšauktas rezervacijas.
