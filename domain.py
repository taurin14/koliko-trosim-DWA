from model import Korisnik,Trosak,Prihod,Izvjesce
from pony.orm import db_session, select
from uuid import uuid4 as gid, UUID



class Korisnici():
    @db_session()
    def izlistavanje():
        u=select (k for k in Korisnik)
        dic = [x.to_dict()  for x in u]
        return dic,

    @db_session()
    def prijava(trenutni_k):
        u=select (k for k in Korisnik)
        dic = [x.to_dict()  for x in u]
        for k in dic:
            if k["Username"] == trenutni_k["Username"] and k["Password"] == trenutni_k["Password"]:
                return k,
        return False
    @db_session()
    def dodavanje(novi):
        try:
            novi["id"]=str(gid())
            novi_korisnik=Korisnik(**novi)
            return True,novi_korisnik.id

        except Exception as e:
            return str(e),False

class Troskovi():
    @db_session()
    def izlistavanje(korisnik_id):
        u=select (t for t in Trosak)
        dic = [x.to_dict()  for x in u]
        t_lista = []
        for d in dic:
            if d["korisnik"] == korisnik_id:
                t_lista.append(d)
        return t_lista,

    @db_session()
    def dodaj_trosak(t):
        try:
            t["id"]=str(gid())
            novi_trosak=Trosak(**t)
            return True,novi_trosak.id

        except Exception as e:
            return str(e),False



class Prihodi():
    @db_session()
    def izlistavanje(korisnik_id):
        u=select (k for k in Prihod)
        dic = [x.to_dict()  for x in u]
        p_lista = []
        for d in dic:
            if d["korisnik"] == korisnik_id:
                p_lista.append(d)
        return p_lista

    @db_session()
    def dodaj_prihod(p):
        try:
            p["id"]=str(gid())
            novi_prihod=Prihod(**p)
            return True, novi_prihod.id

        except Exception as e:
                return str(e),False


class Izvjesca():
    @db_session()
    def izlistavanje(korisnik_id):
        u=select (k for k in Izvjesce)
        dic = [x.to_dict() for x in u]
        i_lista = []
        for d in dic:
            if d["korisnik"] == korisnik_id:
                i_lista.append(d)
        return i_lista,

    @db_session()
    def izracunavanje(korisnik_id):
        ukupni_prihod = 0
        ukupni_trosak = 0
        prihodi = Prihodi.izlistavanje(korisnik_id)
        troskovi = Troskovi.izlistavanje(korisnik_id)
        for p in prihodi:
            ukupni_prihod = ukupni_prihod + p["iznos"]
        for t in troskovi[0]:
            ukupni_trosak = ukupni_trosak + t["iznos"]
        ukupno_stanje = ukupni_prihod - ukupni_trosak
        izvjesce = {
            "ukupno_kraj": ukupno_stanje,
            "ukupno_trosak": ukupni_trosak,
            "ukupni_prihod": ukupni_prihod,
            "korisnik": korisnik_id
        }
        novo_izvjesce = Izvjesca.dodaj_izvjesce(izvjesce)
        return True, novo_izvjesce

    @db_session()
    def dodaj_izvjesce(i):
        try:
            i["id"]=str(gid())
            novi_izvjesce=Izvjesce(**i)
            return True, novi_izvjesce.id

        except Exception as e:
                return str(e),False

print("Dovrsio domain")
