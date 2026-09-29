import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURACIJA ZA GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- GLAVNI EKRAN - SAMO FORMA ZA VOZAČE ---
st.title("🚗 Primopredaja Vozila")
st.write("Popunite listu provere stanja elemenata u vozilu.")

sada_beograd = datetime.now(ZoneInfo("Europe/Belgrade"))
trenutni_datum = sada_beograd.strftime("%Y-%m-%d")
trenutno_vreme = sada_beograd.strftime("%H:%M")

st.info(f"📅 Datum: {trenutni_datum} | ⏰ Vreme: {trenutno_vreme}")
registracija = st.text_input("Registracija vozila (npr. BG 1010 AB)", placeholder="BG _______")

st.markdown("---")
st.subheader("Provera elemenata")

stavke_nazivi = [
    "1. Saobraćajna", "2. Polisa", "3. Zeleni karton (opciono)", "4. Evropski izveštaj",
    "5. Prsluk (u kabini, vozačeva vrata)", "6. Držač za telefon (podešen prema preporuci)",
    "7. Kabl za vozačev telefon (2m C)", "8. Kabl za klijenta (1m C)", "9. Kabl za klijenta (1m iPhone)",
    "10. Voda u držačima", "11. Dve vode u naslonu za ruku", "12. Voda u prtljažniku",
    "13. Vlažne maramice na poziciji", "14. Bezbednosni komplet", "15. Kišobran",
    "16. Buster za decu", "17. Sedište za decu (opciono)", "18. Tablica za docek",
    "19. Dodatak za pojas", "20. TAG", "21. Kartica za rampu",
    "22. Kartica za gorivo", "23. Marker i papir"
]

rezultati_forme = []
for i, naziv in enumerate(stavke_nazivi, start=1):
    cols = st.columns([3, 1])
    with cols[0]:
        status = st.checkbox(naziv, value=True, key=f"ch_{i}")
    
    napomena = ""
    if not status:
        with cols[1]:
            st.warning("Nedostaje")
        napomena = st.text_input(f"Razlog za: {naziv}", key=f"nap_{i}")
        
    rezultati_forme.append("OK" if status else "Nedostaje")
    rezultati_forme.append(napomena)

st.markdown("---")
st.subheader("Podaci o vozačima")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Vozač koji predaje:**")
    p_ime = st.text_input("Ime vozača koji predaje", key="p_ime")
    p_prezime = st.text_input("Prezime vozača koji predaje", key="p_prezime")
    p_tel = st.text_input("Telefon vozača koji predaje", key="p_tel")
with col2:
    st.markdown("**Vozač koji preuzima:**")
    uz_ime = st.text_input("Ime vozača koji preuzima", key="uz_ime")
    uz_prezime = st.text_input("Prezime vozača koji preuzima", key="uz_prezime")
    uz_tel = st.text_input("Telefon vozača koji preuzima", key="uz_tel")

st.markdown("---")
if st.button("Pošalji izveštaj", type="primary", use_container_width=True):
    if not registracija or not p_ime or not uz_ime:
        st.error("Molimo popunite registraciju i imena oba vozača!")
    else:
        vrednosti = [
            trenutni_datum, trenutno_vreme, registracija,
            *rezultati_forme,
            p_ime, p_prezime, p_tel,
            uz_ime, uz_prezime, uz_tel
        ]
        
        # URL Google tablice
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1BhuM_b7K_G8GMUQCDhVSJc8eSHin_-Qfe3mkTWTVuS8/edit"
        
        # Direktno dodavanje novog reda na kraj tablice preko gspread klijenta
        sheet = conn.client.open_by_url(spreadsheet_url).sheet1
        sheet.append_row(vrednosti)
        
        st.success("Uspešno poslato i sačuvano u Google Tabeli!")
        st.balloons()