class Kitap:
    # odunc_verildi_mi=False diyerek varsayılan bir değer atıyoruz
    def __init__(self, kitap_id, isim, yazar, tur, odunc_verildi_mi=False):
        self.kitap_id = kitap_id
        self.isim = isim
        self.yazar = yazar
        self.tur = tur
        self.odunc_verildi_mi = odunc_verildi_mi

    def __str__(self):
        durum = "Ödünçte" if self.odunc_verildi_mi else "Müsait"
        return f"[{self.kitap_id}] {self.isim} - {self.yazar} ({durum})"

class Uye:
    # alinan_kitaplar=[] diyerek liste yapısını karşılıyoruz
    def __init__(self, uye_id, ad_soyad, alinan_kitaplar=None):
        self.uye_id = uye_id
        self.ad_soyad = ad_soyad
        # Eğer dışarıdan liste gelmezse boş liste oluştur
        self.alinan_kitaplar = alinan_kitaplar if alinan_kitaplar is not None else []

    def __str__(self):
        return f"ID: {self.uye_id} | İsim: {self.ad_soyad} | Kitap Sayısı: {len(self.alinan_kitaplar)}"
    # bu nedir #
    # Tamam #