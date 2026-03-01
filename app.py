import streamlit as st
import actions

st.set_page_config(page_title="Balgat Kütüphane Otomasyonu", layout="wide")

def stil_uygula(giris_mi=False):
    if giris_mi:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                            url("https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=1920&q=80");
                background-size: cover;
                background-position: center;
            }
            [data-testid="stForm"] { background-color: rgba(255, 255, 255, 0.9); padding: 30px; border-radius: 15px; max-width: 400px; margin: auto; }
            h1 { color: white !important; text-align: center; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #e0f2fe !important; }
            .header-band { background-color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold; color: #1e3a8a; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            .islem-baslik { background-color: #dcfce7 !important; padding: 15px; border-radius: 10px 10px 0 0; text-align: center; font-weight: bold; color: #166534; border: 1px solid #bbf7d0; margin-bottom: 0px !important; }
            [data-testid="stVerticalBlock"] > div { gap: 0px !important; }
            div.stButton > button { width: 100% !important; background-color: #dcfce7 !important; color: #166534 !important; border: 1px solid #bbf7d0 !important; border-radius: 0px !important; margin: 0px !important; height: 50px; font-weight: bold; }
            div.stButton > button:hover { background-color: #bbf7d0 !important; }
            [data-testid="stSidebar"] { display: none; }
            </style>
        """, unsafe_allow_html=True)

if "giris_basarili" not in st.session_state: st.session_state["giris_basarili"] = False
if "sayfa" not in st.session_state: st.session_state["sayfa"] = "🏠 Genel"
if "admin_kullanici" not in st.session_state: st.session_state["admin_kullanici"] = "admin"
if "admin_sifre" not in st.session_state: st.session_state["admin_sifre"] = "1234"

# --- GİRİŞ EKRANI ---
if not st.session_state["giris_basarili"]:
    stil_uygula(True)
    st.markdown("<br><br><br><h1>🏛️ Balgat Kütüphane Giriş</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2: # Hatalı operatör buradaydı, düzeltildi
        with st.form("giris_formu"):
            k_adi = st.text_input("Kullanıcı Adı")
            sifre = st.text_input("Şifre", type="password")
            if st.form_submit_button("Sisteme Giriş Yap"):
                if k_adi == st.session_state["admin_kullanici"] and sifre == st.session_state["admin_sifre"]:
                    st.session_state["giris_basarili"] = True
                    st.rerun()
                else: st.error("❌ Kullanıcı adı veya şifre hatalı!")

# --- ANA PANEL ---
else:
    stil_uygula(False)
    actions.sistem_baslat()
    st.markdown("<div class='header-band'>🏛️ KÜTÜPHANE YÖNETİM PANELİ</div>", unsafe_allow_html=True)
    
    col_icerik, col_islem = st.columns([0.78, 0.22])

    with col_icerik:
        st.subheader(f"📍 {st.session_state['sayfa']}")
        
        if st.session_state["sayfa"] == "🏠 Genel":
            kitaplar = actions.kitaplari_getir()
            if kitaplar:
                st.table([{"ID": k[0], "Kitap": k[1], "Yazar": k[2], "Tür": k[3], "Durum": "🟢 Müsait" if k[4]==0 else f"🔴 Ödünçte ({k[5]})"} for k in kitaplar])
            else: st.info("Henüz kayıt bulunmuyor.")

        elif st.session_state["sayfa"] == "🆕 Kitap Kayıt":
            with st.container(border=True):
                k_ad = st.text_input("Kitap Adı")
                k_yaz = st.text_input("Yazar")
                k_tur = st.selectbox("Tür", ["Roman", "Bilim Teknik", "Kişisel Gelişim", "Tarih", "Diğer"])
                if st.button("Kitabı Sisteme Ekle"):
                    if k_ad and k_yaz:
                        actions.kitap_ekle(k_ad, k_yaz, k_tur)
                        st.success(f"'{k_ad}' başarıyla eklendi.")
                    else: st.error("Lütfen tüm alanları doldurun.")

        elif st.session_state["sayfa"] == "👤 Üye Kayıt":
            with st.container(border=True):
                u_ad = st.text_input("Ad")
                u_soy = st.text_input("Soyad")
                u_no = st.text_input("Üye Numarası")
                if st.button("Üyeyi Kaydet"):
                    if u_ad and u_soy and u_no:
                        actions.uye_ekle(u_ad, u_soy, u_no)
                        st.success(f"Üye {u_ad} {u_soy} başarıyla kaydedildi.")
                    else: st.error("Lütfen tüm üye bilgilerini girin.")

        elif st.session_state["sayfa"] == "⚙️ Kayıt Yönetimi":
            t1, t2 = st.tabs(["📚 Kitap Düzenle/Sil", "👤 Üye Listesi"])
            with t1:
                kitaplar = actions.kitaplari_getir()
                if kitaplar:
                    secim = st.selectbox("İşlem Yapılacak Kitap", [f"{k[0]}: {k[1]}" for k in kitaplar])
                    k_id = int(secim.split(":")[0])
                    m_k = [k for k in kitaplar if k[0] == k_id][0]
                    
                    yeni_ad = st.text_input("Kitap Adı", value=m_k[1])
                    yeni_yaz = st.text_input("Yazar", value=m_k[2])
                    yeni_tur = st.selectbox("Tür", ["Roman", "Bilim Teknik", "Kişisel Gelişim", "Tarih", "Diğer"])
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("💾 Güncelle"):
                            actions.kitap_guncelle(k_id, yeni_ad, yeni_yaz, yeni_tur)
                            st.success("Bilgiler güncellendi.")
                            st.rerun()
                    with c2:
                        if st.button("🗑️ Kaydı Sil"):
                            actions.kitap_sil(k_id)
                            st.rerun()
                else: st.info("Kayıtlı kitap yok.")
            with t2:
                uyeler = actions.uyeleri_getir()
                if uyeler:
                    st.table([{"No": u[3], "Ad": u[1], "Soyad": u[2]} for u in uyeler])
                else: st.info("Kayıtlı üye yok.")

        elif st.session_state["sayfa"] == "🤝 Ödünç/İade":
            t1, t2 = st.tabs(["📤 Ödünç Ver", "📥 İade Al"])
            with t1:
                kitap_list = [k for k in actions.kitaplari_getir() if k[4] == 0]
                uye_list = actions.uyeleri_getir()
                if kitap_list and uye_list:
                    k_s = st.selectbox("Kitap", [f"{k[0]}: {k[1]}" for k in kitap_list])
                    u_s = st.selectbox("Üye", [f"{u[3]} - {u[1]} {u[2]}" for u in uye_list])
                    if st.button("İşlemi Tamamla"):
                        actions.kitap_odunc_ver(int(k_s.split(":")[0]), u_s, 15)
                        st.success("Kitap verildi.")
                        st.rerun()
            with t2:
                odunc_list = [k for k in actions.kitaplari_getir() if k[4] == 1]
                if odunc_list:
                    i_s = st.selectbox("İade Al", [f"{k[0]}: {k[1]}" for k in odunc_list])
                    if st.button("İadeyi Onayla"):
                        actions.kitap_iade_et(int(i_s.split(":")[0]))
                        st.success("Kitap iade alındı.")
                        st.rerun()

        elif st.session_state["sayfa"] == "🔑 Şifre İşlemleri":
            st.markdown("### 🔐 Bilgileri Güncelle")
            y_k = st.text_input("Yeni Kullanıcı Adı", value=st.session_state["admin_kullanici"])
            y_s = st.text_input("Yeni Şifre", type="password")
            if st.button("Güncelle"):
                st.session_state["admin_kullanici"] = y_k
                st.session_state["admin_sifre"] = y_s
                st.success("Giriş bilgileri güncellendi.")

    with col_islem:
        st.markdown("<div class='islem-baslik'>İŞLEMLER</div>", unsafe_allow_html=True)
        menu = ["🏠 Genel", "🆕 Kitap Kayıt", "👤 Üye Kayıt", "⚙️ Kayıt Yönetimi", "🤝 Ödünç/İade", "🔑 Şifre İşlemleri"]
        for m in menu:
            if st.button(m):
                st.session_state["sayfa"] = m
                st.rerun()
        
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔒 Güvenli Çıkış"):
            st.session_state["giris_basarili"] = False
            st.rerun()