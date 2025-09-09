from models.osnovno_sredstvo_model import OsnovnoSredstvoModel
from views.stampa_izvestaja import StampaIzvestaja
from tkinter import messagebox
from datetime import datetime
import locale


class AmortizacijaController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    ''' Pokretanje otvaranja prozora za pregled amortizacije '''

    def start(self):
        self.view.pokreni(self)

    @staticmethod
    def izracunaj_amortizovanu_vrednost(nabavna, procenat, broj_meseci):
        obracunata_amortizacija = nabavna*procenat/100*broj_meseci/12
        return round(obracunata_amortizacija, 2)

    def izracunaj_broj_meseci_za_amortizaciju(self, status, mesec_amortizacije, umanjenik):
        if status == 'aktivno':
            return mesec_amortizacije-umanjenik
        else:
            return 0

    def koliko_meseci(self, godina_amortizacije, godina_pretposlednje, osnovno_sredstvo, mesec_pretposlednje, mesec_amortizacije):
        if godina_amortizacije == godina_pretposlednje:
            if osnovno_sredstvo[5].year == godina_amortizacije:
                if osnovno_sredstvo[5].month > mesec_pretposlednje:
                    return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[7], mesec_amortizacije, osnovno_sredstvo[5].month)
                else:
                    return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[7], mesec_amortizacije, mesec_pretposlednje)
            else:
                return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[7], mesec_amortizacije, mesec_pretposlednje)
        else:
            if osnovno_sredstvo[5].year == godina_amortizacije:
                return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[7], mesec_amortizacije, osnovno_sredstvo[5].month)
            else:
                return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[7], mesec_amortizacije, 0)

    def podaci_za_izvestaj(self, id_amortizacije):
        os_model1 = OsnovnoSredstvoModel()
        return os_model1.izvestaj_amortizacije(id_amortizacije)

    '''pomocna funkcija za popunjavanje podataka u tabelu izvestaj amortizacije na ekranu'''
    def popuni_tabelu_amortizacije(self, izvestaj):
        locale.setlocale(locale.LC_ALL, 'de_DE')

        # Ovo mora u slucaju da nema podataka, pa da se izbegne prijava greske
        if izvestaj is not None:
            self.view.my_tree_amortizacija.delete(*self.view.my_tree_amortizacija.get_children())
            # Ovde idu podaci iz stavki naloga i prikazuju se u tabeli

            self.view.my_tree_amortizacija.tag_configure('oddrow', background="white")
            self.view.my_tree_amortizacija.tag_configure('evenrow', background="lightblue")
            self.view.my_tree_amortizacija.tag_configure('ukupnorow', background="#5887C2", foreground="white", font=('Helvetica', 10, 'bold'))
            # self.podaci_tabela.set(rezultat_stavke)
            count_stavke_naloga = 0

            ukupno_opreme = 0
            ukupno_nabavna_vrednost = 0
            ukupno_amortizacija = 0
            ukupno_dosadasnji_otpis = 0
            ukupno_ukupni_otpis = 0
            ukupno_nova_sadasnja = 0

            for record in izvestaj:

                nabavna_vrednost = locale.format_string('%10.2f', record[3], grouping=True)
                amortizacija = locale.format_string('%10.2f', record[4], grouping=True)
                dosadasnji_otpis = locale.format_string('%10.2f', record[5], grouping=True)
                ukupni_otpis = locale.format_string('%10.2f', record[6], grouping=True)
                nova_sadasnja = locale.format_string('%10.2f', record[7], grouping=True)

                if count_stavke_naloga % 2 == 0:
                    self.view.my_tree_amortizacija.insert(parent='', index='end', iid=count_stavke_naloga, text='',
                                                      values=(record[0], record[1], record[2], nabavna_vrednost,
                                                              amortizacija, dosadasnji_otpis, ukupni_otpis,
                                                              nova_sadasnja),
                                                      tags=('evenrow',))
                else:
                    self.view.my_tree_amortizacija.insert(parent='', index='end', iid=count_stavke_naloga, text='',
                                                      values=(record[0], record[1], record[2], nabavna_vrednost,
                                                              amortizacija, dosadasnji_otpis, ukupni_otpis,
                                                              nova_sadasnja),
                                                      tags=('oddrow',))
                count_stavke_naloga += 1
                ukupno_opreme += record[2]
                ukupno_nabavna_vrednost += record[3]
                ukupno_amortizacija += record[4]
                ukupno_dosadasnji_otpis += record[5]
                ukupno_ukupni_otpis += record[6]
                ukupno_nova_sadasnja += record[7]

            ukupno_opreme_format = ukupno_opreme
            ukupno_nabavna_vrednost_format = locale.format_string('%10.2f', ukupno_nabavna_vrednost, grouping=True)
            ukupno_amortizacija_format = locale.format_string('%10.2f', ukupno_amortizacija, grouping=True)
            ukupno_dosadasnji_otpis_format = locale.format_string('%10.2f', ukupno_dosadasnji_otpis, grouping=True)
            ukupno_ukupni_otpis_format = locale.format_string('%10.2f', ukupno_ukupni_otpis, grouping=True)
            ukupno_nova_sadasnja_format = locale.format_string('%10.2f', ukupno_nova_sadasnja, grouping=True)

            self.view.my_tree_amortizacija.insert('', 'end', values=("", "UKUPNO", ukupno_opreme_format, ukupno_nabavna_vrednost_format, ukupno_amortizacija_format, ukupno_dosadasnji_otpis_format, ukupno_ukupni_otpis_format, ukupno_nova_sadasnja_format), tags=('ukupnorow',))

    def uradi_obracun_amortizacije(self, id_amortizacije, os_za_amortizaciju, mesec_amortizacije, godina_amortizacije, mesec_pretposlednje, godina_pretposlednje):

        for osnovno_sredstvo in os_za_amortizaciju:
            ''' za koliko meseci se radi amortizacija za ovo osnovno sredstvo'''
            broj_meseci_za_amort = self.koliko_meseci(godina_amortizacije, godina_pretposlednje, osnovno_sredstvo, mesec_pretposlednje, mesec_amortizacije)
            # print("broj meseci za amortizaciju osnovnog sredstva " + str(osnovno_sredstvo[1]) + " je " + str(broj_meseci_za_amort))
            stvarna_amort = self.izracunaj_amortizovanu_vrednost(osnovno_sredstvo[2], osnovno_sredstvo[4], broj_meseci_za_amort)
            trenutna_vrednost_os = osnovno_sredstvo[2]-(osnovno_sredstvo[3] + stvarna_amort)
            if trenutna_vrednost_os <= 0:
                obracunata_amort = stvarna_amort + trenutna_vrednost_os
                amortizovano = 'da'
            else:
                obracunata_amort = stvarna_amort
                amortizovano = 'ne'

            ''' OVDE TREBA POPUNITI TABELU u bazi podataka amortizacija_opreme'''
            self.model.unesi_u_tabelu_amortizacija_opreme(id_amortizacije, osnovno_sredstvo[0], float(obracunata_amort), float(stvarna_amort))
            ''' **** azurirati otpisanu vrednost osnovnog sredstva u tabeli osnovna sredstva '''
            os_model = OsnovnoSredstvoModel()
            nova_otpisana_vrednost = osnovno_sredstvo[3] + obracunata_amort
            os_model.azuriraj_otpisanu_vrednost(osnovno_sredstvo[0], nova_otpisana_vrednost, amortizovano)
            ''' OVDE TREBA POPUNITI TABELU IZVESTAJ AMORTIZACIJE '''
            os_model.unesi_podatke_u_izvestaj(osnovno_sredstvo[6], float(osnovno_sredstvo[2]), float(obracunata_amort), float(osnovno_sredstvo[3]), id_amortizacije, osnovno_sredstvo[0])
        ''' OVDE TREBA IZVUCI PODATKE ZA IZVESTAJ URADJENE AMORTIZACIJE'''
        self.view.amortizacija_id.set(id_amortizacije)
        izvestaj = self.podaci_za_izvestaj(id_amortizacije)
        ''' POPUNJAVANJE TABELE NA EKRANU - IZVESTAJ AMORTIZACIJE'''
        self.popuni_tabelu_amortizacije(izvestaj)

    @staticmethod
    def pronadji_aktivna_os(datum):
        os_model = OsnovnoSredstvoModel()
        return os_model.pronadji_osnovna_sredstva_amortizacija(datum)

    def racunaj_amortizaciju(self):
        # otvara prozor sa prikazom progresa
        datum = self.view.datum_amortizacije.get_date()
        godina_amortizacije = datum.year
        mesec_amortizacije = datum.month
        provera = self.model.da_li_postoji_amortizacija_posle_datuma(datum, mesec_amortizacije, godina_amortizacije)
        datum_amortizacije = datum.strftime('%Y-%m-%d')
        ''' proveri da li ima uradjena amortizacija posle ovog datuma - ako ima ne moze se raditi amortizacija, ako nema uneti datum u tabele AMORTIZACIJA '''
        if provera:
            messagebox.showwarning("Greška", "Već ima uradjena amortizacija za ovaj mesec ili posle njega!",
                                   parent=self.view.amortizacija_frame)
        else:
            ''' kreirati novi zapis u tabeli AMORTIZACIJA sa ovim datumom '''

            kreirano = datetime.now()
            # broj_naloga = "amortizacija"+"_" + str(mesec_amortizacije) + "_" + str(godina_amortizacije) + "_" + str(kreirano)
            broj_naloga = "amortizacija" + "_" + datum_amortizacije
            kreirana_amortizacija = kreirano.strftime("%Y-%m-%d, %H:%M:%S")
            self.model.kreiraj_amortizaciju(datum_amortizacije, broj_naloga, kreirana_amortizacija)
            # pronadji poslednji zapis u tabeli AMORTIZACIJA da bi se uzeo ID koji ce se uneti u tabelu AMORTIZACIJA_OPREME
            poslednja_amortizacija = self.model.pronadji_poslednji_zapis_amortizacije_u_tabeli()
            id_poslednje_amortizacije = poslednja_amortizacija[0][0]
            pretposlednja_amortizacija = self.model.pronadji_pretposlednji_zapis_amortizacije_u_tabeli()

            if pretposlednja_amortizacija:
                godina_pretposlednje_amortizacije = pretposlednja_amortizacija[0][0].year
                mesec_pretposlednje_amortizacije = pretposlednja_amortizacija[0][0].month
            else:
                godina_pretposlednje_amortizacije = 0
                mesec_pretposlednje_amortizacije = 0
            ''' pronadji sva aktivna osnovna sredstva '''
            os_za_amortizaciju = self.pronadji_aktivna_os(datum)
            self.uradi_obracun_amortizacije(id_poslednje_amortizacije, os_za_amortizaciju, mesec_amortizacije, godina_amortizacije, mesec_pretposlednje_amortizacije, godina_pretposlednje_amortizacije)

    def stampanje_amortizacije(self):
        id_amortizacije = self.view.amortizacija_id.get()
        podaci_za_stampu = self.podaci_za_izvestaj(id_amortizacije)
        ''' podaci o uradjenoj amortizacijji '''
        podaci_o_amortizaciji = self.model.pronadji_amortizaciju(id_amortizacije)
        ''' slanje podataka na stampu '''
        try:
            stampa = StampaIzvestaja()
            stampa.stampa_izvestaja_amortizacije(podaci_za_stampu, podaci_o_amortizaciji)
        except OSError:
            messagebox.showwarning("Greška", "Morate zatvoriti prethodni PDF izveštaj amortizacije!", parent=self.view.amortizacija_frame)

    def spisak_amortizacija(self):
        ''' pronadji sve uradjene amortizacije sortirane po id '''
        return self.model.pronadji_sve_uradjene_amortizacije()

    def list_sve_amortizacije(self):
        # Brisanje tabele zbog azuriranja
        self.view.my_tree_sve_amortizacije.delete(*self.view.my_tree_sve_amortizacije.get_children())
        # povezivanje na bazu i preuzimanje dobavljaca iz tabele
        rezultat = self.spisak_amortizacija()

        count_amortizacije = 0
        for record in rezultat:

            if count_amortizacije % 2 == 0:
                self.view.my_tree_sve_amortizacije.insert(parent='', index='end', iid=record[0], text='',
                                                        values=(record[2].capitalize(), record[1].strftime("%d.%m.%Y")), tags=('evenrow',))
            else:
                self.view.my_tree_sve_amortizacije.insert(parent='', index='end', iid=record[0], text='',
                                                        values=(record[2].capitalize(), record[1].strftime("%d.%m.%Y")), tags=('oddrow',))
            count_amortizacije += 1

    ''' Selektovanje reda u tabeli '''
    def izaberi_red_amortizacije(self, e):
        # Uzeti identifikator reda
        return self.view.my_tree_sve_amortizacije.focus()

    def izabrana_amortizacija(self):
        id_amortizacije = self.izaberi_red_amortizacije(e=None)
        if id_amortizacije == "":
            messagebox.showwarning("Hmmmm", "Niste ništa izabrali!",
                                   parent=self.view.prozor_spisak_amortizacija)
        else:
            izvestaj = self.podaci_za_izvestaj(id_amortizacije)
            podaci_amortizacija = self.model.pronadji_amortizaciju(id_amortizacije)
            self.view.amortizacija_id.set(id_amortizacije)
            ''' POPUNJAVANJE TABELE NA EKRANU - IZVESTAJ AMORTIZACIJE'''
            self.popuni_tabelu_amortizacije(izvestaj)
            self.view.naziv_amortizacije.config(text=podaci_amortizacija[0][2].capitalize() + " od " + podaci_amortizacija[0][1].strftime("%d.%m.%Y"))
            self.view.prozor_spisak_amortizacija.destroy()

    def poruka_brisanje(self):
        # Pronalazenje ID amortizacije na osnovu klika
        selected = self.view.my_tree_sve_amortizacije.focus()
        if selected:
            # Pronadji poslednju amortizaciju
            pronadjena_amortizacija = self.model.pronadji_poslednji_zapis_amortizacije_u_tabeli()
            # Provera da li je proknjizen nalog, ako je proknjizen nema brisanja
            if pronadjena_amortizacija[0][0] == int(selected):
                self.view.prozor_za_brisanje(selected)
            else:
                messagebox.showwarning("Upozorenje.", "Možete da obrišete samo poslednju amortizaciju.", parent=self.view.prozor_spisak_amortizacija)
        else:
            messagebox.showwarning("Greška", "Hmmmmm, niste izabrali amortizaciju za brisanje!", parent=self.view.prozor_spisak_amortizacija)

    def obrisi_amortizaciju(self, id_amortizacije):
        ''' obrisati podatke iz izvestaj_amortizacije'''
        self.model.obrisi_izvestaj_amortizacije(id_amortizacije)
        ''' obrisati podatke iz amortizacija_opreme '''
        ''' pre brisanja podataka iz tabele uzeti vrednosti id opreme i obracunata amortizacija zbog azuriranja dosadasnjeg otpisa u tabeli osnovna sredstva'''
        rezultat = self.model.pronadji_otpisane_vrednosti(id_amortizacije)
        self.model.obrisi_amortizacija_opreme(id_amortizacije)
        ''' obrisati podatke iz tabela amortizacija '''
        self.model.obrisi_amortizacija(id_amortizacije)
        ''' azurirati vrednosti dosadasnji otpis u tabeli osnovna sredstva '''
        os_model = OsnovnoSredstvoModel()
        for red in rezultat:
            pronadjen_os = os_model.pronadji_os_po_id(red[0])
            umanjena_vrednost = pronadjen_os[0][4] - red[1]
            ''' ovde se proverava da li amotizovano osnovno sredstvo  posle brisanja amortizacije nije vise amortizovano, vraca se u aktivno'''
            if pronadjen_os[0][3] > umanjena_vrednost:
                os_model.azuriraj_otpisanu_vrednost_brisanje_amortizacije(red[0], umanjena_vrednost, "aktivno")
            else:
                os_model.azuriraj_otpisanu_vrednost_brisanje_amortizacije(red[0], umanjena_vrednost, stat=None)

        self.view.my_tree_amortizacija.delete(*self.view.my_tree_amortizacija.get_children())
        ''' skloniti dijalog box - Da li zelite da obrisete amortizaciju '''
        self.view.prozor_brisanje.destroy()

        ''' azurirati tabelu sa spiskom amortizacija '''
        self.list_sve_amortizacije()
