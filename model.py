from pony.orm import Database, PrimaryKey, Required, Set, db_session, Optional
from uuid import uuid4 as gid, UUID
import datetime as dt



db = Database()



db.bind(provider='sqlite', filename='baza.sqlite', create_db=True)

class Korisnik(db.Entity):
    id= PrimaryKey(str)
    Ime = Required(str)
    Prezime= Required(str)
    Adresa = Required(str)
    Username = Required(str)
    Password = Required(str)
    korisnik_trosak= Set("Trosak")
    korisnik_prihod= Set("Prihod")
    korisnik_izvjesce= Set("Izvjesce")


print("Zavrsio korisnika")

class Trosak(db.Entity):
    id= PrimaryKey(str)
    naziv = Required(str)
    iznos = Required(float)
    opis = Required(str)
    korisnik = Required(Korisnik)

class Prihod(db.Entity):
    id= PrimaryKey(str)
    naziv = Required(str)
    iznos = Required(float)
    opis = Required(str)
    korisnik = Required(Korisnik)

class Izvjesce(db.Entity):
    id=PrimaryKey(str)
    ukupno_kraj= Optional(float)
    ukupno_trosak = Optional(float)
    ukupni_prihod = Optional(float)
    korisnik = Required(Korisnik)
print("Zavrsio bazu")

db.generate_mapping(check_tables=True, create_tables=True)
