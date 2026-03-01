import sqlite3
from datetime import datetime, timedelta

def sistem_baslat():
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    # Kitaplar tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS kitaplar 
                 (id INTEGER PRIMARY KEY, ad TEXT, yazar TEXT, tur TEXT, odunc_durumu INTEGER, iade_tarihi TEXT)''')
    # Üyeler tablosu (Ad, Soyad, Üye No eklendi)
    c.execute('''CREATE TABLE IF NOT EXISTS uyeler 
                 (id INTEGER PRIMARY KEY, ad TEXT, soyad TEXT, uye_no TEXT)''')
    conn.commit()
    conn.close()

def kitaplari_getir():
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("SELECT * FROM kitaplar")
    veriler = c.fetchall()
    conn.close()
    return veriler

def uyeleri_getir():
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("SELECT * FROM uyeler")
    veriler = c.fetchall()
    conn.close()
    return veriler

def kitap_ekle(ad, yazar, tur):
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("INSERT INTO kitaplar (ad, yazar, tur, odunc_durumu) VALUES (?, ?, ?, 0)", (ad, yazar, tur))
    conn.commit()
    conn.close()

def uye_ekle(ad, soyad, uye_no):
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("INSERT INTO uyeler (ad, soyad, uye_no) VALUES (?, ?, ?)", (ad, soyad, uye_no))
    conn.commit()
    conn.close()

def kitap_guncelle(k_id, ad, yazar, tur):
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("UPDATE kitaplar SET ad=?, yazar=?, tur=? WHERE id=?", (ad, yazar, tur, k_id))
    conn.commit()
    conn.close()

def kitap_sil(k_id):
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("DELETE FROM kitaplar WHERE id=?", (k_id,))
    conn.commit()
    conn.close()

def kitap_odunc_ver(k_id, u_id, gun):
    iade_t = (datetime.now() + timedelta(days=gun)).strftime('%d.%m.%Y')
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("UPDATE kitaplar SET odunc_durumu=1, iade_tarihi=? WHERE id=?", (iade_t, k_id))
    conn.commit()
    conn.close()

def kitap_iade_et(k_id):
    conn = sqlite3.connect('kutuphane.db')
    c = conn.cursor()
    c.execute("UPDATE kitaplar SET odunc_durumu=0, iade_tarihi=NULL WHERE id=?", (k_id,))
    conn.commit()
    conn.close()