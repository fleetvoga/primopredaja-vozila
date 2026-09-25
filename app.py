import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
<<<<<<< HEAD
import pandas as pd
import io
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURACIJA ZA GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- MAPIRANJE SKRAĆENIH NAZIVA ZA PRIKAZ ---
skraceni_nazivi = {
    "datum": "Datum",
    "vreme": "Vreme",
    "registracija": "Reg",
    "stavka_1_saobracajna": "1. S", "napomena_1": "N.1",
    "stavka_2_polisa": "2. P", "napomena_2": "N.2",
    "stavka_3_zeleni_karton": "3. ZK", "napomena_3": "N.3",
    "stavka_4_evropski_izvestaj": "4. EI", "napomena_4": "N.4",
    "stavka_5_prsluk": "5. Prs", "napomena_5": "N.5",
    "stavka_6_drzac_za_telefon": "6. Drz", "napomena_6": "N.6",
    "stavka_7_kabl_vozac": "7. KabV", "napomena_7": "N.7",
    "stavka_8_kabl_klijent_c": "8. KabC", "napomena_8": "N.8",
    "stavka_9_kabl_klijent_iphone": "9. KabI", "napomena_9": "N.9",
    "stavka_10_voda_drzaci": "V_DR", "napomena_10": "N.10",
    "stavka_11_voda_naslon": "V_NAS", "napomena_11": "N.11",
    "stavka_12_voda_prtljaznik": "V_PRT", "napomena_12": "N.12",
    "stavka_13_vlazne_maramice": "V_MAR", "napomena_13": "N.13",
    "stavka_14_bezbednosni_komplet": "BEZ", "napomena_14": "N.14",
    "stavka_15_kisobran": "KIS", "napomena_15": "N.15",
    "stavka_16_buster": "BUS", "napomena_16": "N.16",
    "stavka_17_sediste": "SED", "napomena_17": "N.17",
    "stavka_18_tablica_docek": "TAB", "napomena_18": "N.18",
    "stavka_19_dodatak_pojas": "POJ", "napomena_19": "N.19",
    "stavka_20_tag": "TAG", "napomena_20": "N.20",
    "stavka_21_kartica_rampa": "RAM", "napomena_21": "N.21",
    "stavka_22_kartica_gorivo": "GOR", "napomena_22": "N.22",
    "stavka_23_marker_i_papir": "MAR", "napomena_23": "N.23",
    "predaje_ime": "P_Ime", "predaje_prezime": "P_Prz", "predaje_telefon": "P_Tel",
    "preuzima_ime": "U_Ime", "preuzima_prezime": "U_Prz", "preuzima_telefon": "U_Tel"
}

st.sidebar.title("Navigacija")
izbor = st.sidebar.radio("Izaberite opciju:", ["📝 Nova primopredaja (Vozači)", "📊 Admin Pregled (Samo za Vas)"])

if izbor == "📝 Nova primopredaja (Vozači)":
    st.title("🚗 Primopredaja Vozila")
    st.write("Popunite listu provere stanja elemenata u vozilu.")

    # Uzimamo tačno lokalno vreme za Beograd umesto UTC vremena servera
    sada_beograd = datetime.now(ZoneInfo("Europe/Belgrade"))
    trenutni_datum = sada_beograd.strftime("%Y-%m-%d")
    trenutno_vreme = sada_beograd.strftime("%H:%M")

    st.info(f"📅 Datum: {trenutni_datum} | ⏰ Vreme: {trenutno_vreme}")
    registracija = st.text_input("Registracija vozila (npr. BG 1010 AB)", placeholder="BG _______")

    st.markdown("---")
    st.subheader("Provera elemenata")
=======
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

<<<<<<< HEAD
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
            kolone_redosled = [
                "datum", "vreme", "registracija",
                "stavka_1_saobracajna", "napomena_1", "stavka_2_polisa", "napomena_2",
                "stavka_3_zeleni_karton", "napomena_3", "stavka_4_evropski_izvestaj", "napomena_4",
                "stavka_5_prsluk", "napomena_5", "stavka_6_drzac_za_telefon", "napomena_6",
                "stavka_7_kabl_vozac", "napomena_7", "stavka_8_kabl_klijent_c", "napomena_8",
                "stavka_9_kabl_klijent_iphone", "napomena_9", "stavka_10_voda_drzaci", "napomena_10",
                "stavka_11_voda_naslon", "napomena_11", "stavka_12_voda_prtljaznik", "napomena_12",
                "stavka_13_vlazne_maramice", "napomena_13", "stavka_14_bezbednosni_komplet", "napomena_14",
                "stavka_15_kisobran", "napomena_15", "stavka_16_buster", "napomena_16",
                "stavka_17_sediste", "napomena_17", "stavka_18_tablica_docek", "napomena_18",
                "stavka_19_dodatak_pojas", "napomena_19", "stavka_20_tag", "napomena_20",
                "stavka_21_kartica_rampa", "napomena_21", "stavka_22_kartica_gorivo", "napomena_22",
                "stavka_23_marker_i_papir", "napomena_23",
                "predaje_ime", "predaje_prezime", "predaje_telefon",
                "preuzima_ime", "preuzima_prezime", "preuzima_telefon"
            ]
            
            vrednosti = [
                trenutni_datum, trenutno_vreme, registracija,
                *rezultati_forme,
                p_ime, p_prezime, p_tel,
                uz_ime, uz_prezime, uz_tel
            ]
            
            novi_df = pd.DataFrame([vrednosti], columns=kolone_redosled)
            existing_df = conn.read(ttl="0s")
            updated_df = pd.concat([existing_df, novi_df], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success("Uspešno poslato i sačuvano u Google Tabeli!")
            st.balloons()

elif izbor == "📊 Admin Pregled (Samo za Vas)":
    st.title("🔐 Admin Panel")
    lozinka = st.text_input("Unesite lozinku za pristup bazi:", type="password")

    if lozinka != "admin123":
        if lozinka != "":
            st.error("Pogrešna lozinka!")
        st.stop()

    st.success("Lozinka je tačna!")
    st.subheader("Pregled svih sačuvanih izveštaja")

    try:
        df = conn.read(ttl="0s")

        if df.empty:
            st.info("Google Tabela je trenutno prazna. Još uvek nema poslatih izveštaja.")
        else:
            # Skraćivanje napomena na samo prvu reč za pregled
            df_prikaz = df.copy()
            for kolona in df_prikaz.columns:
                if kolona.startswith("napomena_"):
                    df_prikaz[kolona] = df_prikaz[kolona].astype(str).apply(
                        lambda x: x.split()[0] if x != "nan" and x.strip() != "" else ""
                    )

            # Preimenovanje kolona prema rečniku skraćenica
            df_prikaz = df_prikaz.rename(columns=skraceni_nazivi)

            st.write(f"Ukupno unetih izveštaja: {len(df_prikaz)}")
            st.dataframe(df_prikaz, use_container_width=True)

            # Dugme za preuzimanje originalnog Excel-a
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Primopredaje')
            processed_data = output.getvalue()

            st.download_button(
                label="📥 Preuzmi kompletan Excel izveštaj (.xlsx)",
                data=processed_data,
                file_name=f"Evidencija_Vozila_{datetime.now(ZoneInfo('Europe/Belgrade')).strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
    except Exception as e:
        st.error(f"Došlo je do greške prilikom čitanja Google Tabele: {e}")
=======
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

