import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- KONFIGURACIJA ZA GOOGLE SHEETS PREKO GSPREAD ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def povezi_se_na_sheets():
    creds_dict = json.loads(st.secrets["gcp_json"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BhuM_b7K_G8GMUQCDhVSJc8eSHin_-Qfe3mkTWTVuS8/edit?gid=0#gid=0") 
    return sh.get_worksheet(0)

# --- FUNKCIJA ZA SLANJE EMAIL OBAVEŠTENJA ---
def posalji_email_obavestenje(registracija, datum, vreme, p_ime, p_prezime, uz_ime, uz_prezime):
    try:
        sender_email = st.secrets["EMAIL_SADRZAJ"]
        sender_password = st.secrets["EMAIL_PASS"]
        receiver_email = st.secrets["EMAIL_PRIMALAC"]

        subject = f"🔔 Nova primopredaja vozila: {registracija}"
        body = f"""
        Poštovani,
        
        Izvršena je nova primopredaja vozila:

        🚗 Registracija: {registracija}
        📅 Datum i vreme: {datum} u {vreme}
        
        👤 Predaje: {p_ime} {p_prezime}
        👤 Preuzima: {uz_ime} {uz_prezime}
        
        Pregledajte Google Tabelu za detalje.
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Greška pri slanju emaila: {e}")

# --- DODATNI CSS ZA ESTETIKU I KRUPNIJA SLOVA ---
st.set_page_config(page_title="Primopredaja Vozila", layout="wide")
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    html, body, [class*="css"] {
        font-size: 1.15rem !important;
    }
    div[data-testid="stTextInput"] input[placeholder*="BG"] {
        font-size: 1.6rem !important;
        font-weight: bold !important;
        height: 3.2rem !important;
        letter-spacing: 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- GLAVNI EKRAN ZA UNOS ---
st.title("🚗 Primopredaja Vozila")
st.write("Popunite listu provere stanja elemenata u vozilu.")

# Uzimamo tačno lokalno vreme za Beograd
sada_beograd = datetime.now(ZoneInfo("Europe/Belgrade"))
trenutni_datum = sada_beograd.strftime("%d-%m-%Y")
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
    "19. Dodatak za pojas", "20. TAG", "21. Kartica za rampu"
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
        try:
            sheet = povezi_se_na_sheets()
            sheet.append_row(vrednosti, table_range='A1')
            
            # Slanje email obaveštenja sa tačnim lokalnim vremenom
            posalji_email_obavestenje(registracija, trenutni_datum, trenutno_vreme, p_ime, p_prezime, uz_ime, uz_prezime)
            
            st.success("Uspešno poslato!!!")
            st.balloons()
        except Exception as e:
            st.error(f"Došlo je do greške pri upisu u tabelu: {e}")
