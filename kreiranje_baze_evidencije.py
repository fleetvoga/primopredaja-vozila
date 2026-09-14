import sqlite3

def kreiraj_bazu():
    # Povezivanje na SQLite bazu (pravi fajl "evidencija_vozila.db" u trenutnom folderu)
    konekcija = sqlite3.connect('evidencija_vozila.db')
    kursor = konekcija.cursor()

    # Kreiranje tabele sa svim traženim poljima
    kursor.execute('''
        CREATE TABLE IF NOT EXISTS primopredaja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            vreme TEXT NOT NULL,
            registracija TEXT NOT NULL,
            
            -- 21 stavka (status: npr. "OK" ili "Nedostaje", i napomena uz svaku)
            stavka_1_saobracajna TEXT, napomena_1 TEXT,
            stavka_2_polisa TEXT, napomena_2 TEXT,
            stavka_3_zeleni_karton TEXT, napomena_3 TEXT,
            stavka_4_evropski_izvestaj TEXT, napomena_4 TEXT,
            stavka_5_prsluk TEXT, napomena_5 TEXT,
            stavka_6_drzac_za_telefon TEXT, napomena_6 TEXT,
            stavka_7_kabl_vozac TEXT, napomena_7 TEXT,
            stavka_8_kabl_klijent_c TEXT, napomena_8 TEXT,
            stavka_9_kabl_klijent_iphone TEXT, napomena_9 TEXT,
            stavka_10_voda_drzaci TEXT, napomena_10 TEXT,
            stavka_11_voda_naslon TEXT, napomena_11 TEXT,
            stavka_12_voda_prtljaznik TEXT, napomena_12 TEXT,
            stavka_13_vlazne_maramice TEXT, napomena_13 TEXT,
            stavka_14_bezbednosni_komplet TEXT, napomena_14 TEXT,
            stavka_15_kisobran TEXT, napomena_15 TEXT,
            stavka_16_buster TEXT, napomena_16 TEXT,
            stavka_17_sediste TEXT, napomena_17 TEXT,
            stavka_18_tablica_docek TEXT, napomena_18 TEXT,
            stavka_19_dodatak_pojas TEXT, napomena_19 TEXT,
            stavka_20_tag TEXT, napomena_20 TEXT,
            stavka_21_kartica_rampa TEXT, napomena_21 TEXT,
            
            -- Vozač koji predaje vozilo
            predaje_ime TEXT NOT NULL,
            predaje_prezime TEXT NOT NULL,
            predaje_telefon TEXT NOT NULL,
            
            -- Vozač koji preuzima vozilo
            preuzima_ime TEXT NOT NULL,
            preuzima_prezime TEXT NOT NULL,
            preuzima_telefon TEXT NOT NULL
        )
    ''')

    konekcija.commit()
    konekcija.close()
    print("Uspešno kreirana SQLite baza 'evidencija_vozila.db' i tabela 'primopredaja'!")

if __name__ == "__main__":
    kreiraj_bazu()