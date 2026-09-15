import streamlit as st
from datetime import datetime
import pandas as pd
import io
import gspread
from google.oauth2.service_account import Credentials

# --- KONFIGURACIJA ZA GOOGLE SHEETS PREKO GSPREAD ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def povezi_se_na_sheets():
    # Uzima kredencijale direktno iz Streamlit Secrets (ceo gcp_service_account ili gsheet sekcija)
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    # Ovde upisi tacno ime tvoje Google tabele
    sh = gc.open("Evidencija opreme za vozila") 
    return sh.get_worksheet(0)

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
    "predaje_ime": "P_Ime", "predaje_prezime": "P_Prz", "predaje_telefon": "P_Tel",
    "preuzima_ime": "U_Ime", "preuzima_prezime": "U_Prz", "preuzima_telefon": "U_Tel"
}

st.sidebar.title("Navigacija")
izbor = st.sidebar.radio("Izaberite opciju:", ["📝 Nova primopredaja (Vozači)", "📊 Admin Pregled (Samo za Vas)"])

if izbor == "📝 Nova primopredaja (Vozači)":
    st.title("🚗 Primopredaja Vozila")
    st.write("Popunite listu provere stanja elemenata u vozilu.")

    trenutni_datum = datetime.now().strftime("%Y-%m-%d")
    trenutno_vreme = datetime.now().strftime("%H:%M")

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
                sheet.append_row(vrednosti)
                st.success("Uspešno poslato i sačuvano u Google Tabeli!")
                st.balloons()
            except Exception as e:
                st.error(f"Greška pri upisu u tabelu: {e}")

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
        sheet = povezi_se_na_sheets()
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            st.info("Google Tabela je trenutno prazna. Još uvek nema poslatih izveštaja.")
        else:
            # Skraćivanje napomena na samo prvu reč za pregled
            df_prikaz = df.copy()
            for kolona in df_prikaz.columns:
                if str(kolona).startswith("napomena_"):
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
                file_name=f"Evidencija_Vozila_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
    except Exception as e:
        st.error(f"Došlo je do greške prilikom čitanja Google Tabele: {e}")
