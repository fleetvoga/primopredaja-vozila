import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Dozvole za Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def povezi_se_na_sheets():
    creds_dict = json.loads(st.secrets["gcp_json"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    # Vežemo se direktno na tvoju tabelu
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BhuM_b7K_G8GMUQCDhVSJc8eSHin_-Qfe3mkTWTVuS8/edit?gid=0#gid=0")
    return sh.get_worksheet(0)

def posalji_email_obavestenje(registracija, datum, vreme, p_ime, p_prezime, uz_ime, uz_prezime):
    sender_email = st.secrets["EMAIL_SADRZAJ"]
    sender_password = st.secrets["EMAIL_PASS"]
    receiver_email = st.secrets["EMAIL_PRIMALAC"]

    subject = f"🔔 Nova primopredaja vozila: {registracija}"
    body = f"""Poštovani,
    
Izvršena je nova primopredaja vozila:

🚗 Registracija: {registracija}
📅 Datum i vreme: {datum} u {vreme}

👤 Predaje: {p_ime} {p_prezime}
👤 Preuzima: {uz_ime} {uz_prezime}

Pregledajte Google Tabelu za detalje."""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

# --- GLAVNI DEO APLIKACIJE ---
st.title("🚗 Evidencija primopredaje vozila")

with st.form("form_primopredaja"):
    registracija = st.text_input("Registracija vozila")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Vozač koji predaje")
        p_ime = st.text_input("Ime (predaje)")
        p_prezime = st.text_input("Prezime (predaje)")
    with col2:
        st.subheader("Vozač koji preuzima")
        uz_ime = st.text_input("Ime (preuzima)")
        uz_prezime = st.text_input("Prezime (preuzima)")
        
    submit_button = st.form_submit_button(label="Pošalji izveštaj")

if submit_button:
    if not registracija or not p_ime or not uz_ime:
        st.warning("Molimo popunite obavezna polja (registracija i imena vozača)!")
    else:
        try:
            # 1. Upis u tabelu tačno od kolone A
            sheet = povezi_se_na_sheets()
            sada = datetime.now()
            datum_str = sada.strftime("%Y-%m-%d")
            vreme_str = sada.strftime("%H:%M")
            
            red_podataka = [datum_str, vreme_str, registracija, p_ime, p_prezime, uz_ime, uz_prezime]
            sheet.append_row(red_podataka, table_range='A1')
            
            # 2. Slanje email obaveštenja
            posalji_email_obavestenje(registracija, datum_str, vreme_str, p_ime, p_prezime, uz_ime, uz_prezime)
            
            st.success("Uspešno sačuvano u Google Tabeli i poslat email!")
        except Exception as e:
            st.error(f"Došlo je do greške: {e}")
