from flask import Flask, Response, jsonify, request, render_template, json
from domain import Korisnici,Troskovi,Prihodi,Izvjesca
from  flask_cors import CORS



app = Flask(__name__)
CORS(app)

trenutni_korisnik_g = []
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prijava',methods=['POST','GET'] )
def prijava():
    global trenutni_korisnik_g
    if request.method == 'GET':
        return render_template('prijava.html')
    elif request.method == 'POST':
        trenutni_korisnik = {
            "Username": request.form["Username"],
            "Password": request.form["Password"]
        }
        status = Korisnici.prijava(trenutni_korisnik)
        if status == False:
            r = Response(status=500)
            return r
        else:

            trenutni_korisnik_g = status
            troskovi= Troskovi.izlistavanje(trenutni_korisnik_g[0]["id"])
            prihodi= Prihodi.izlistavanje(trenutni_korisnik_g[0]["id"])
            izvjesce = Izvjesca.izlistavanje(trenutni_korisnik_g[0]["id"])

            if prihodi == [] and troskovi[0] == []:
                return render_template('profil.html', korisnik=status)
            elif prihodi == []:
                return render_template('profil.html', korisnik=status, troskovi=troskovi[0])
            elif troskovi[0] == []:
                return render_template('profil.html', korisnik=status, prihodi=prihodi)

            else:
                return render_template('profil.html', troskovi=troskovi[0], prihodi=prihodi, izvjesce=izvjesce[0], korisnik=status)





@app.route('/korisnici',methods=['POST','GET'])
def korisnici():
    if request.method == 'GET':
        return render_template('registracija.html')
    elif request.method == 'POST':
        novi_korisnik = {
            "Ime": request.form["Ime"],
            "Prezime": request.form["Prezime"],
            "Adresa": request.form["Adresa"],
            "Username": request.form["Username"],
            "Password": request.form["Password"]
        }
        status,greske = Korisnici.dodavanje(novi_korisnik)
        if status:
            return render_template('index.html')
        else:
            r = Response(status=500)
            r.set_data(greske)
            return r


@app.route('/prihodi/<id>',methods = ['POST','PUT'])
def prihodi(id):
    if request.method == 'POST':
        prihod = {
            "naziv": request.form["Naziv"],
            "iznos": request.form["Iznos"],
            "opis": request.form["Opis"],
            "korisnik": id
        }
        status,greske = Prihodi.dodaj_prihod(prihod)
        Izvjesca.izracunavanje(id)
        troskovi= Troskovi.izlistavanje(id)
        prihodi= Prihodi.izlistavanje(id)
        izvjesce = Izvjesca.izlistavanje(id)
        if status:

            return render_template('profil.html', korisnik=trenutni_korisnik_g, troskovi=troskovi[0], prihodi=prihodi, izvjesce=izvjesce[0])
        else:
            r=Response(status=500)
            return r
    elif  request.method =='PUT':
        status,greske = Prihodi.update_prihode(request.get_json())
        if status:
            return Response(status=202)
        else:
            r=Response(status=500)
            r.set_data(greske)
            return r

@app.route('/troskovi/<id>',methods = ['POST','PUT'])
def troskovi(id):
    if request.method == 'POST':
        trosak = {
            "naziv": request.form["Naziv"],
            "iznos": request.form["Iznos"],
            "opis": request.form["Opis"],
            "korisnik": id
        }
        status,greske = Troskovi.dodaj_trosak(trosak)
        Izvjesca.izracunavanje(id)
        troskovi= Troskovi.izlistavanje(id)
        prihodi= Prihodi.izlistavanje(id)
        izvjesce = Izvjesca.izlistavanje(id)
        if status:
            return render_template('profil.html', korisnik=trenutni_korisnik_g, troskovi=troskovi[0], prihodi=prihodi, izvjesce=izvjesce[0])
        else:
            r=Response(status=500)
            return r
    elif  request.method =='PUT':
        status,greske = Troskovi.update_trosak(request.get_json())
        if status:
            return Response(status=202)
        else:
            r=Response(status=500)
            r.set_data(greske)
            return r

@app.route('/izvjesca/<id>',methods=['GET'] )
def izvjesca(id):
    return render_template('unos_troskova.html', id=id)


if __name__ == '__main__':
    app.debug = True
    app.run()
