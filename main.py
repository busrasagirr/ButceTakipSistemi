from flask import Flask, session, escape, redirect, render_template, request, url_for, jsonify
import sqlite3
#import requests
# session modülü ile kullanıcı giriş bilgilerini tutuyorum!
# escape modülü session dan gelen bilgileri ekrana döndürmek amaçlı kullanılıyor.


# KULLANICI İŞLEMLERİ:

#Kullanıcı Ekleme:
def kullaniciEkle(ad, soyad, telefon, mail, sifre):
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("insert into BT_Kullanicilar (Ad,Soyad,Telefon,Mail,Sifre) values (?,?,?,?,?)", (ad,soyad,telefon,mail,sifre))
        con.commit()
    print("Kullanıcı Eklendi!")

kullanicilar = []

#Kullanıcıları listeye çekme:
def kullaniciAl(id):
    global kullanicilar
    #global sessionKullaniciID
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("select * from BT_Kullanicilar where KullaniciID=? order by KullaniciID desc",(id,))
        #cur.execute("select * from BT_Kullanicilar where KullaniciID=? order by KullaniciID desc",(sessionKullaniciID))
        kullanicilar = cur.fetchall()
        #for i in kullanicilar:
            #print(i)

#Kullanici Silme:
def kullaniciSil(id):
    global kullanicilar
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("delete from BT_Kullanicilar where KullaniciID=?",id)
        kullanicilar = cur.fetchall()
    print("Kullanıcı Silindi !")

#Kullanıcı Güncelleme:
def kullaniciGuncelle(id,ad,soyad,telefon,mail,sifre):
    global kullanicilar
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("update BT_Kullanicilar set Ad=?, Soyad=?, Telefon=?, Mail=?,Sifre=? where KullaniciID=?", (ad,soyad,telefon,mail,sifre,id))
        con.commit()
    print("Kullanıcı Güncellendi !")

#kullaniciAl() 

#  GELİR - GİDER İŞLEMLERİ:

# Gelir/Gider Ekleme:
def hareketEkle(kullaniciID, kategoriID, tutar, tarih):
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("insert into BT_Hareketler (KullaniciID, KategoriID, Tutar, Tarih) values (?,?,?,?)", (kullaniciID, kategoriID, tutar, tarih))
        con.commit()
    print("Hareket Eklendi!")

hareketler = []
# api için:
def hareketAlApi():
    global hareketler 
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("select * from BT_Hareketler order by HareketID desc")
        hareketler = cur.fetchall()
#Gelir/Gider listeye çekme:
def hareketAl(id):
    global hareketler 
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("select h.HareketID, kul.Ad,kul.Soyad,k.Kategori,k.GelirGider,h.Tutar,h.Tarih,k.KategoriID from BT_Hareketler as h inner join BT_Kullanicilar as kul on h.KullaniciID = kul.KullaniciID inner join BT_Kategoriler as k on h.KategoriID = k.KategoriID where h.KullaniciID=? order by HareketID desc",(id,))
        hareketler = cur.fetchall()
        #for i in hareketler:
            #print(i)

def hareketAl2(secim, id):
    global hareketler2
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("select h.HareketID, kul.Ad,kul.Soyad,k.Kategori,k.GelirGider,h.Tutar,h.Tarih, k.KategoriID from BT_Hareketler as h inner join BT_Kullanicilar as kul on h.KullaniciID = kul.KullaniciID inner join BT_Kategoriler as k on h.KategoriID = k.KategoriID where h.KullaniciID=? and k.GelirGider=? order by HareketID desc",(id, secim,))
        hareketler2 = cur.fetchall()        

#Gelir/Gider Güncelle:
def hareketGuncelle(id,kullaniciID,kategoriID,tarih,tutar):
    global hareketler
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("update BT_Hareketler set KullaniciID=?, KategoriID=?, Tarih=?, Tutar=? where HareketID=?", (kullaniciID, kategoriID, tarih, tutar, id))
        con.commit()
    print("Hareket Güncellendi !")

# Gelir/Gider Sil:
def hareketSil(id):
    global hareketler
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("delete from BT_Hareketler where HareketID=?", (id,))
        con.commit()
        #hareketler = cur.fetchall()
    print("Hareket Silindi!")

#hareketAl()

#-------------------------------Kategoriler-------------------------------------------
# Başka sayfalarda kullanmak için:
def kategoriAl(secim):
    global kategoriler
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        if secim != "Tümü":
            cur.execute("select * from BT_Kategoriler where GelirGider=? order by KategoriID desc",(secim,))
        else:
            cur.execute("select * from BT_Kategoriler order by KategoriID desc")
        kategoriler = cur.fetchall()
        #for i in kategoriler:
            #print(i)

kategoriler = []

# Kategoriler sayfasında görüntülemek için:
def kategoriEkle(kategori,gelirGider):
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("insert into BT_Kategoriler (Kategori,GelirGider) values (?,?)", (kategori,gelirGider))
        con.commit()
    print("Kategori Eklendi!")

kategoriler2 = []

def kategoriListele():
    global kategoriler2
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("select * from BT_Kategoriler order by KategoriID desc")
        kategoriler2 = cur.fetchall()

def kategoriSil(id):
    global kategoriler2
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("delete from BT_Kategoriler where KategoriID=?", (id,))
        con.commit()
        #kategoriler2 = cur.fetchall()
    print("Kategori Silindi!")

def kategoriGuncelle(id,kategori,gelirGider):
    global kategoriler2
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        cur.execute("update BT_Kategoriler set Kategori=?, GelirGider=? where KategoriID=?", (kategori, gelirGider, id))
        con.commit()
    print("Kategori Güncellendi !")


#------------------------------------------------------------
girisBilgileri = []
#girisliste = []

def Login(isim, sifre):
    global girisBilgileri, sessionKullaniciID
    with sqlite3.connect("ButceTakipDB.db") as con:
        cur = con.cursor()
        try:
            cur.execute("select * from BT_Kullanicilar where Mail=? and Sifre=?",(isim, sifre))
            girisBilgileri = cur.fetchall()
            if girisBilgileri == []:
                print("veri tabanından boş döndü !")
                return redirect(url_for("login"))
        except:
            print("veri tabanı sorgu hatası!")
            return redirect(url_for("login"))
        girisliste = []
        for i in girisBilgileri:
            girisliste.append(i[0])
            girisliste.append(i[1])
            girisliste.append(i[2])
            girisliste.append(i[3])
            girisliste.append(i[4])
            girisliste.append(i[5])
    print(girisliste)
            
    if girisliste[4] == isim and girisliste[5] == sifre:
        session['kullaniciAd'] = isim
        session['kullaniciID'] = girisliste[0]
        sessionKullaniciID = girisliste[0]
        return sessionKullaniciID
    else:
        print("giriş yapılamadı!")
        return redirect(url_for("login"))





# ------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Qr8z\n\xec]/'


@app.route("/")
def anasayfa():    
    if 'kullaniciID' in session:
        return render_template("anasayfa.html")        
    else:
        return redirect(url_for("login"))
    #-----------Session ın çalıştığını test ettim!-----------
    #if 'isim' in session:
        #return 'Merhaba %s' % escape(session['isim'])
    #return 'Giriş yapmadınız!'
    #---------------------------------------------------------
    

@app.route("/giris", methods=['GET','POST'])   # Kullanıcı girişi !
def login():
    if request.method == 'POST':
        isim = request.form['isim']
        sifre = request.form['sifre']
        #print(session['isim'],session['sifre'])
        Login(isim, sifre)
        print(isim ,sifre)
        return redirect(url_for('anasayfa'))
    #return render_template("giris.html")
    else:
        return render_template("giris.html")

@app.route("/cikis")     # Çıkış yapmak !
def logout():
    session.pop('isim', None)
    session.pop('sifre', None)
    session.pop('kullaniciID', None)
    session.pop('kullaniciAd', None)
    return redirect(url_for('login'))

@app.route("/contact")
def contact():
    if 'kullaniciID' in session:
        return render_template("contact.html")        
    else:
        return redirect(url_for("login"))

#----------------Kullanıcı İşlemleri--------------------------------

@app.route("/KullaniciDetay/<string:id>")    
def KullaniciDetay(id):
    if 'kullaniciID' in session:   
        kDetay = []
        for d in kullanicilar:
            if str(d[0]) == id:
                kDetay = list(d)
        return render_template("KullaniciDetay.html",veri=kDetay)
    else:
        return redirect(url_for("login"))

@app.route("/KullaniciDuzenle/<string:id>", methods=["GET","POST"])
def KullaniciDuzenle(id):
    if 'kullaniciID' in session:
        if request.method == "POST":
            id = request.form["KullaniciID"]
            Ad = request.form["Ad"]
            Soyad = request.form["Soyad"]
            Telefon = request.form["Telefon"]
            Mail = request.form["Mail"]
            Sifre = request.form["Sifre"]
            print("Güncellenecek Veriler: ",Ad, Soyad, Telefon, Mail, Sifre)
            kullaniciGuncelle(id,Ad, Soyad, Telefon, Mail, Sifre)
            return redirect(url_for("Kullanicilar"))
        else:
            guncellenecekKullanici = []
            for k in kullanicilar:
                if str(k[0]) == id:
                    guncellenecekKullanici = list(k)
            return render_template("KullaniciDuzenle.html", veri=guncellenecekKullanici)
    else:
        return redirect(url_for("login"))

@app.route("/KullaniciEkle", methods=["POST","GET"])
def KullaniciEkle():
    if 'kullaniciID' in session:
        if request.method == "POST":
            Ad = request.form["Ad"]
            Soyad = request.form["Soyad"]
            Telefon = request.form["Telefon"]
            Mail = request.form["Mail"]
            Sifre = request.form["Sifre"]

            print("eklencekKullanıcı: ",Ad, Soyad, Telefon, Mail, Sifre)
            kullaniciEkle(Ad, Soyad, Telefon, Mail, Sifre)
        
        return render_template("KullaniciEkle.html")
    else:
        return redirect(url_for("login"))

@app.route("/Kullanicilar")
def Kullanicilar():
    if 'kullaniciID' in session:
        kullaniciAl(session['kullaniciID']) 
        return render_template("Kullanicilar.html",veri=kullanicilar)
    else:
        return redirect(url_for("login"))

@app.route("/KullaniciSil/<string:id>")
def KullaniciSil(id):
    if 'kullaniciID' in session:
        kullaniciSil(id)
        return redirect(url_for("Kullanicilar"))
    else:
        return redirect(url_for("login"))

#-------------KATEGORİLER---------------------------
@app.route("/KategoriEkle",methods=["GET","POST"])
def KategoriEkle():
    if 'kullaniciID' in session:
        if request.method == "GET":
            #kategoriAl("Tümü")
            return render_template("KategoriEkle.html")
        if request.method == "POST":
            kategori = request.form["Kategori"]
            gelirGider = request.form["GelirGider"]

            print("eklencekKullanıcı: ",kategori, gelirGider)
            kategoriEkle(kategori, gelirGider)
        return  render_template("KategoriEkle.html")
    else:
        return redirect(url_for("login"))

@app.route("/Kategoriler")
def Kategoriler():
    if 'kullaniciID' in session:
        kategoriListele()
        return render_template("Kategoriler.html",veri=kategoriler2)
    else:
        return redirect(url_for("login"))

@app.route("/KategoriSil/<string:id>")
def KategoriSil(id):
    if 'kullaniciID' in session:
        kategoriSil(id)
        return redirect(url_for("Kategoriler"))
    else:
        return redirect(url_for("login"))

@app.route("/KategoriDuzenle/<string:id>", methods=["GET","POST"])
def KategoriDuzenle(id):
    if 'kullaniciID' in session:
        if request.method == "POST":
            id = request.form["KategoriID"]
            kategori = request.form["Kategori"]
            gelirGider = request.form["GelirGider"]
            kategoriGuncelle(id,kategori,gelirGider)
            return redirect(url_for("Kategoriler"))
        else:
            guncellenecekKategori = []
            for d in kategoriler2:
                if str(d[0]) == id:
                    guncellenecekKategori = list(d)
            return render_template("KategoriDuzenle.html",veri=guncellenecekKategori)
    else:
        return redirect(url_for("login"))


#----------GELİR-GİDER İŞLEMLERİ------------------------
@app.route("/HareketEkle", methods=["POST","GET"])
def HareketEkle():
    if 'kullaniciID' in session:
        if request.method == "GET":
            kategoriAl("Tümü")
            return render_template("HareketEkle.html", veri2=kategoriler)
        if request.method == "POST":
            kategoriAl("Tümü")
            kullaniciID = session["kullaniciID"]   # giriş yapan kullanıcıya kaydediyor!
            #kategoriID = request.form["KategoriID"]
            tarih = request.form["Tarih"]
            tutar = request.form["Tutar"]
            kategori = request.form["Kategori"]
            #kategoriID = request.form["KategoriID"]
            kategoriDoldur = []
            with sqlite3.connect("ButceTakipDB.db") as con:
                cur = con.cursor()
                cur.execute("select * from BT_Kategoriler where Kategori=? order by KategoriID desc",(kategori,))
                kategoriDoldur = cur.fetchall()                
                for i in kategoriDoldur:
                    if i[0]:
                        kategoriID = i[0]

            print("eklencek hareket: ",kullaniciID, kategoriID, tutar, tarih)
            hareketEkle(kullaniciID, kategoriID, tutar, tarih)
        kategoriAl("Tümü")
        return render_template("HareketEkle.html")
    else:
        return redirect(url_for("login"))

@app.route("/Hareketler",methods=['GET','POST'])
def Hareketler():
    if 'kullaniciID' in session:
        if request.method == "GET":
            hareketAl(session['kullaniciID'])  
            kategoriAl("Tümü")
            return render_template("Hareketler.html", veri=hareketler,veri2=kategoriler)
        else:
            secim = request.form['secim']
            if secim != "Tümü":
                hareketAl2(secim, session['kullaniciID'])
                kategoriAl(secim)
                return render_template("Hareketler.html", veri=hareketler2, veri2=kategoriler)
            else:
                hareketAl(session['kullaniciID'])
                kategoriAl("Tümü")
                return render_template("Hareketler.html", veri=hareketler,veri2=kategoriler)
    else:
        return redirect(url_for("login"))

@app.route("/HareketDetay/<string:id>")
def HareketDetay(id):
    if 'kullaniciID' in session:
        detayHareket = []
        for d in hareketler:
            if str(d[0]) == id :
                detayHareket = list(d)
        return render_template("HareketDetay.html",veri=detayHareket)
    else:
        return redirect(url_for("login"))        


@app.route("/HareketDuzenle/<string:id>", methods=["GET","POST"])
def HareketDuzenle(id):
    if 'kullaniciID' in session:
        if request.method == "POST":
            id = request.form["HareketID"]
            kullaniciID = session["kullaniciID"]
            #kategoriID = request.form["KategoriID"]
            tarih = request.form["Tarih"]
            tutar = request.form["Tutar"]
            kategori = request.form["Kategori"]
            kategoriDoldur = []
            with sqlite3.connect("ButceTakipDB.db") as con:
                cur = con.cursor()
                cur.execute("select * from BT_Kategoriler where Kategori=? order by KategoriID desc",(kategori,))
                kategoriDoldur = cur.fetchall()                
                for i in kategoriDoldur:
                    if i[0]:
                        kategoriID = i[0]

            hareketGuncelle(id,kullaniciID,kategoriID,tarih,tutar)
            return redirect(url_for("Hareketler"))
        else:
            guncellenecekHareket = []
            for d in hareketler:
                if str(d[0]) == id:
                    guncellenecekHareket = list(d)
                    print(guncellenecekHareket)
            return render_template("HareketDuzenle.html",veri=guncellenecekHareket)
    else:
        return redirect(url_for("login"))

@app.route("/HareketSil/<string:id>")
def HareketSil(id):
    if 'kullaniciID' in session:
        hareketSil(id)
        return redirect(url_for("Hareketler"))
    else:
        return redirect(url_for("login"))

# ------------------- API ----------------------

@app.route("/api", methods=["GET"])
def api():
    hareketAlApi()
    print(hareketler)
    veri = [{'HareketID': str(row[0]), 'KullaniciID': str(row[1]), 'KategoriID': str(row[2]), 'Tutar': row[3], 'Tarih':row[4]} for row in hareketler]
    return jsonify(veri)

@app.route("/api/add", methods=["POST"])
def apiAdd():
    kullaniciID = request.form['KullaniciID']
    kategoriID = request.form['KategoriID']
    tarih = request.form['Tarih']
    tutar = request.form['Tutar']
    hareketEkle(kullaniciID,kategoriID,tutar,tarih)

    message = 'Yeni hareket başarıyla kaydedildi!'

    return jsonify({'status': 'success', 'result':message})

@app.route("/api/delete/<string:id>", methods=["DELETE"]) 
def apiDelete(id):
    hareketSil(id)

    message = 'Hareket başarıyla silindi!'

    return jsonify({'status': 'success', 'result': message})

@app.route("/api/update/<string:id>", methods=["PUT"])
def apiUpdate(id):
    id = request.form["HareketID"]
    kullaniciID = request.form["KullaniciID"]
    kategoriID = request.form["KategoriID"]
    tarih = request.form["Tarih"]
    tutar = request.form["Tutar"]
    hareketGuncelle(id,kullaniciID,kategoriID,tarih,tutar)

    message = 'Hareket başarıyla güncellendi!'

    return jsonify({'status': 'success', 'result': message})


# http method   (api için)
# POST - Veri ekleyeveğimiz
# GET - veri talep ediyorsunuz
# PUT - update
# DELETE - silmek

#-------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)