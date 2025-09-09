from tkinter import messagebox
from models.dobavljaci_model import DobavljaciModel
from models.konto_model import KontoModel
from models.mesta_model import MestaModel
from models.stope_model import StopeModel
from models.amortizacija_model import AmortizacijaModel
from models.osnovno_sredstvo_model import OsnovnoSredstvoModel
from models.korisnici_model import KorisniciModel
from controllers.keyboard_controller import KeyboardController
from mysql.connector import Error
from views.greske import Greske
from models.nalog_unos_model import NalogUnosModel
from views.stampa_izvestaja import StampaIzvestaja
from datetime import date


class UnosController:
    def __init__(self, view):
        self.view = view
    ''' Pokretanje otvaranja prozora za unos naloga unosa osnovnih sredstava '''
    def start(self):
        self.view.pokreni(self)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_naziv(self, event):
        if self.view.naziv_entry.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latiničnu tastaturu!!",
                                       parent=self.view.prozor_nabavka)
                self.view.naziv_entry.delete(0, 'end')

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_broj_fakture(self, event):
        if self.view.broj_fakture.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latiničnu tastaturu!!",
                                       parent=self.view.master)
                self.view.broj_fakture.delete(0, 'end')

    # Provera da li u polju nabavna vrednost su uneta slova - moraju samo brojevi, i pravljenje dva decimalna mesta
    def provera_broj_nabavna(self, event=None):
        # propusta ako nije nista uneto da ne bi izlazila poruka
        if not self.view.nabavna_entry.get() == '':
            # Konvertuje zarez u tacku, kod unosa brojeva duguje
            ucitan_broj = self.view.nabavna_entry.get()
            promenjeno = ucitan_broj.replace(',', '.')
            # Overwrite the Entrybox content using the widget's own methods
            self.view.nabavna_entry.delete(0, 'end')
            self.view.nabavna_entry.insert(0, promenjeno)
            try:
                float(self.view.nabavna_entry.get())
            except ValueError:
                self.view.nabavna_entry.delete(0, 'end')
                messagebox.showwarning("Greska", "Morate uneti brojeve!!", parent=self.view.prozor_nabavka)
            else:
                # pravljenje dva decimalna mesta
                prom = float(self.view.nabavna_entry.get())
                promenjen_broj = "{:.2f}".format(prom)
                self.view.nabavna_entry.delete(0, 'end')
                self.view.nabavna_entry.insert(0, promenjen_broj)

    # Provera da li u polju otpisana vrednost su uneta slova - moraju samo brojevi, i pravljenje dva decimalna mesta
    def provera_broj_otpisana(self, event=None):
        # propusta ako nije nista uneto da ne bi izlazila poruka
        if not self.view.otpisana_entry.get() == '':
            # Konvertuje zarez u tacku, kod unosa brojeva duguje
            ucitan_broj = self.view.otpisana_entry.get()
            promenjeno = ucitan_broj.replace(',', '.')
            # Overwrite the Entrybox content using the widget's own methods
            self.view.otpisana_entry.delete(0, 'end')
            self.view.otpisana_entry.insert(0, promenjeno)
            try:
                float(self.view.otpisana_entry.get())
            except ValueError:
                self.view.otpisana_entry.delete(0, 'end')
                messagebox.showwarning("Greska", "Morate uneti brojeve!!", parent=self.view.prozor_nabavka)
            else:
                # pravljenje dva decimalna mesta
                prom = float(self.view.otpisana_entry.get())
                promenjen_broj = "{:.2f}".format(prom)
                self.view.otpisana_entry.delete(0, 'end')
                self.view.otpisana_entry.insert(0, promenjen_broj)

    def sve_nabavke(self):
        # Brisanje tabele zbog popunjavanja tabele podacima iza baze - sve stavke naloga za taj nalog
        self.view.my_tree_pregled_nabavki.delete(*self.view.my_tree_pregled_nabavki.get_children())
        # pronalazenje u bazi svih ulaznih faktura
        nab_model = NalogUnosModel()
        data = nab_model.pronadji_sve_nabavke()

        self.view.my_tree_pregled_nabavki.tag_configure('oddrow', background="white")
        self.view.my_tree_pregled_nabavki.tag_configure('evenrow', background="lightblue")
        self.view.my_tree_pregled_nabavki.tag_configure('neproknjizen', background="#ffcbcb")

        count_nalozi = 1
        for record in data:
            if count_nalozi % 2 == 0:
                if record[4] == 1:
                    self.view.my_tree_pregled_nabavki.insert(parent='', index='end', iid=record[0], text='', values=(
                                    count_nalozi, record[1], record[2], record[3].strftime("%d.%m.%Y."), "Da"),
                                    tags=('evenrow',))
                else:
                    self.view.my_tree_pregled_nabavki.insert(parent='', index='end', iid=record[0], text='', values=(
                        count_nalozi, record[1], record[2], record[3].strftime("%d.%m.%Y."), "Ne"),
                                        tags=('neproknjizen',))
            else:
                if record[4] == 1:
                    self.view.my_tree_pregled_nabavki.insert(parent='', index='end', iid=record[0], text='', values=(
                                    count_nalozi, record[1], record[2], record[3].strftime("%d.%m.%Y."), "Da"),
                                    tags=('oddrow',))
                else:
                    self.view.my_tree_pregled_nabavki.insert(parent='', index='end', iid=record[0], text='', values=(
                        count_nalozi, record[1], record[2], record[3].strftime("%d.%m.%Y."), "Ne"),
                                        tags=('neproknjizen',))
            count_nalozi += 1

        # Ova komanda pomera scroll na kraj tabele da bi se videlo koji je poslednji slog unet (dobra stvar:)
        self.view.my_tree_pregled_nabavki.yview_moveto(1)

    def pregledaj_nalog_nabavke(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_pregled_nabavki.focus()
        if selected:
            self.view.otvori_prozor_nabavke(selected)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedan dokument!!", parent=self.view.master)

    @staticmethod
    def pronadji_poslednje_os():
        os = OsnovnoSredstvoModel()
        rezultat = os.pronadji_poslednji()
        return rezultat

    def generisi_inv_broj(self):
        poslednji_inv_broj = self.pronadji_poslednje_os()
        if poslednji_inv_broj[0][0] is None:
            novi_inv_broj = 1
        else:
            novi_inv_broj = int(poslednji_inv_broj[0][0]) + 1
        self.view.inventarni_broj_entry.delete(0, 'end')
        self.view.inventarni_broj_entry.insert(0, novi_inv_broj)

    ''' Pomocna metoda za dobijanje dictionary dobavljaca iz baze podataka '''

    @staticmethod
    def dictionary_svih_dobavljaca():
        dobavljaci_model = DobavljaciModel()
        dobavljaci = dobavljaci_model.read()
        dobavljaci_lista = {}
        for i in dobavljaci:
            dobavljaci_lista[i[0]] = i[1]
        return dobavljaci_lista

    ''' Pomocna metoda za dobijanje naziva dobavljaca iz dictionary'''

    @staticmethod
    def lista_svih_dobavljaca(kljucevi_vrednosti):
        vrednosti = kljucevi_vrednosti.values()
        lista = []
        for i in vrednosti:
            lista.append(i)
        return lista

    ''' Pomocna metoda za dobijanje id dobavljaca iz dictionary dobavljaca'''

    def dobijanje_id_dobavljaca(self):
        dictionary_dobavljaca = self.dictionary_svih_dobavljaca()
        izabrana_vrednost = self.view.unet_naziv_dobavljaca.get()
        id_dobavljaca = [k for k, v in dictionary_dobavljaca.items() if v == izabrana_vrednost]
        if not id_dobavljaca:
            return ""
        else:
            return id_dobavljaca[0]

    ''' Funkcija koja brise nule u polju nabavna vrednost kada se klikne na to polje, a ne brise ako je uneta neka druga vrednost'''

    def brisanje_nula_nabavna(self, e):
        vrednost_polja = self.view.uneta_nabavna_vrednost.get()
        if vrednost_polja == '0,00':
            self.view.uneta_nabavna_vrednost.delete(0, 'end')

    ''' Funkcija koja brise nule u polju otpisana vrednost kada se klikne na to polje, a ne brise ako je uneta neka druga vrednost'''

    def brisanje_nula_otpisana(self, e):
        vrednost_polja = self.view.uneta_otpisana_vrednost.get()
        if vrednost_polja == '0,00':
            self.view.uneta_otpisana_vrednost.delete(0, 'end')

    ''' Pomocna metoda za dobijanje dictionary svih konta iz baze podataka'''

    @staticmethod
    def dictionary_svih_konta():
        konta_model = KontoModel()
        konta = konta_model.read()
        konta_lista = {}
        for i in konta:
            konta_lista[i[0]] = i[1]
        return konta_lista

    ''' Pomocna metoda za dobijanje naziva konta iz dictionary '''

    @staticmethod
    def lista_svih_konta(kljucevi_vrednosti):
        vrednosti = kljucevi_vrednosti.values()
        lista = []
        for i in vrednosti:
            lista.append(i)
        return lista

    ''' Pomocna metoda za dobijanje id konta iz dictionary konta'''

    def dobijanje_id_konta(self):
        dictionary_konta = self.dictionary_svih_konta()
        izabrana_vrednost = self.view.konto_combo.get()
        id_konta = [k for k, v in dictionary_konta.items() if v == izabrana_vrednost]
        if not id_konta:
            return ""
        else:
            return id_konta[0]

    ''' Pomocna metoda za dobijanje dictionary svih lokacija iz baze podataka'''

    @staticmethod
    def dictionary_svih_lokacija():
        mesta_model = MestaModel()
        mesta = mesta_model.read()
        mesta_lista = {}
        for i in mesta:
            mesta_lista[i[0]] = i[1]
        return mesta_lista

    ''' Pomocna metoda za dobijanje naziva lokacija iz dictionary '''

    @staticmethod
    def lista_svih_lokacija(kljucevi_vrednosti):
        vrednosti = kljucevi_vrednosti.values()
        lista = []
        for i in vrednosti:
            lista.append(i)
        return lista

    ''' Pomocna metoda za dobijanje id konta iz dictionary konta'''

    def dobijanje_id_lokacije(self):
        dictionary_lokacije = self.dictionary_svih_lokacija()
        izabrana_vrednost = self.view.izabrana_lokacija.get()
        id_lokacije = [k for k, v in dictionary_lokacije.items() if v == izabrana_vrednost]
        if not id_lokacije:
            return ""
        else:
            return id_lokacije[0]

    ''' Pomocna metoda za dobijanje dictionary svih zaposlenih iz baze podataka za zaduzenje osnovnog sredstva'''

    @staticmethod
    def dictionary_svih_zaposlenih():
        zaposleni_model = KorisniciModel()
        zaposleni = zaposleni_model.read()
        zaposleni_lista = {}
        for i in zaposleni:
            zaposleni_lista[i[0]] = i[1]
        return zaposleni_lista

    ''' Pomocna metoda za dobijanje imena zaposlenih iz dictionary '''

    @staticmethod
    def lista_svih_zaposlenih(kljucevi_vrednosti):
        vrednosti = kljucevi_vrednosti.values()
        lista = []
        for i in vrednosti:
            lista.append(i)
        return lista

    ''' Pomocna metoda za dobijanje id zaposlenog iz dictionary zaposleni'''

    def dobijanje_id_zaposlenog(self):
        dictionary_zaposleni = self.dictionary_svih_zaposlenih()
        izabrana_vrednost = self.view.zaduzenje_combo.get()
        id_zaposlenog = [k for k, v in dictionary_zaposleni.items() if v == izabrana_vrednost]
        if not id_zaposlenog:
            return ""
        else:
            return id_zaposlenog[0]

    ''' Prikaz liste svih stopa iz baze '''

    def list_sve_stope(self):
        # povezivanje na bazu i preuzimanje stopa iz tabele
        stope = StopeModel()
        rezultat = stope.read()
        count_stope = 0
        for record in rezultat:
            if count_stope % 2 == 0:
                self.view.my_tree_sve_stope.insert(parent='', index='end', iid=record[0], text='',
                                              values=(record[1], record[2], record[3]),
                                              tags=('evenrow',))
            else:
                self.view.my_tree_sve_stope.insert(parent='', index='end', iid=record[0], text='',
                                              values=(record[1], record[2], record[3]),
                                              tags=('oddrow',))
            count_stope += 1

    @staticmethod
    def pronadji_stopu(idstope):
        stope = StopeModel()
        rezultat = stope.find_stopa(idstope)
        return rezultat

    ''' Izbor amortizacione stope kod unosa osnovnih sredstava '''

    def izaberi_stopu(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_sve_stope.focus()
        if selected:
            izabrana_stopa = self.pronadji_stopu(selected)
            self.view.stopa_label_iznos.config(text=izabrana_stopa[0][0])
            self.view.id_izabrane_stope.set(selected)
            self.view.prozor_izbor_stope.destroy()
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednu stopu!!", parent=self.view.prozor_izbor_stope)

    def ocisti_polja_unos(self):
        self.view.inventarni_broj_entry.delete(0, 'end')
        self.view.naziv_entry.delete(0, 'end')
        self.view.nabavna_entry.delete(0, 'end')
        self.view.otpisana_entry.delete(0, 'end')
        self.view.konto_combo.set("")
        self.view.status_combo.current(0)
        self.view.stopa_label_iznos.config(text="")
        self.view.izabrana_lokacija.current(0)
        self.view.zaduzenje_combo.current(0)

    def postoji_amortizacija_posle_datuma(self, datum):
        amo_model = AmortizacijaModel()
        pronadji = amo_model.amortizacija_posle_datuma(datum)
        return pronadji

    def proveri_postoji_os_inv_broj(self, inv_broj):
        os_model = OsnovnoSredstvoModel()
        return os_model.postoji_osnovno_sredstvo(inv_broj)

    def proknjizi_osnovno_sredstvo(self):
        ''' OSTALE PROVERE '''
        inv_broj = self.view.inventarni_broj_entry.get()
        if inv_broj.isnumeric():
            pronadjeno_os_inv_broj = self.proveri_postoji_os_inv_broj(inv_broj)
            if pronadjeno_os_inv_broj:
                messagebox.showwarning("Greška", "Već postoji osnovno sredstvo sa ovim inventarnim brojem!", parent=self.view.prozor_nabavka)
            else:
                provera_broj = self.provera_da_li_je_uneto(inv_broj, "inventarni broj")
                naziv = self.view.naziv_entry.get()
                provera_naziv = self.provera_da_li_je_uneto(naziv, "naziv")
                nabavna = self.view.nabavna_entry.get()
                provera_nabavna = self.provera_da_li_je_uneto(nabavna, "nabavna")
                nab = nabavna.replace(",", ".")
                if nab == '0.00' or nab == '0' or nab == "":
                    nabavna_vrednost = float(0)
                else:
                    nabavna_vrednost = float(nab)
                otpis = self.view.otpisana_entry.get()
                otpis_vrednost = otpis.replace(",", ".")
                if otpis_vrednost == '0.00' or otpis_vrednost == '0' or otpis_vrednost == "":
                    otpisana_vrednost = float(0)
                else:
                    otpisana_vrednost = float(otpis_vrednost)
                id_konta = self.dobijanje_id_konta()
                provera_konta = self.provera_da_li_je_uneto(id_konta, "konto")
                status = self.view.status_combo.get()
                provera_status = self.provera_da_li_je_uneto(status, "status")
                stopa = self.view.id_izabrane_stope.get()
                provera_stopa = self.provera_da_li_je_uneto(stopa, "stopa")
                id_lokacije = self.dobijanje_id_lokacije()
                zaposleni = self.dobijanje_id_zaposlenog()
                id_fakture = self.view.faktura
                aktiviran = 0
                if ((provera_broj and provera_status and provera_naziv and provera_konta and provera_nabavna) is False) or provera_stopa == 0:
                    messagebox.showinfo("Obaveštenje", "Osnovno sredstvo nije uneto", parent=self.view.prozor_nabavka)
                else:
                    try:
                        model = OsnovnoSredstvoModel()
                        model.unos_novog_osnovnog_sredstva(int(inv_broj), naziv.upper(), nabavna_vrednost, otpisana_vrednost, status,
                                                               id_konta, stopa, zaposleni, id_lokacije, id_fakture, aktiviran, otpisana_vrednost)
                        self.ocisti_polja_unos()
                        self.prikazi_opremu_tabela_nabavke(id_fakture)
                        self.view.inventarni_broj_entry.focus()
                    except Error as e:
                        Greske("Problem unosa osnovnog sredstva u bazu - OsnovnoSredstvoModel-unos_novog_osnovnog_sredstva", e)
                        messagebox.showwarning("Hmmmmmmmmmm", "Nešto nije u redu!", parent=self.view.prozor_nabavka)
        else:
            messagebox.showwarning("Greška", "Inventarni broj može da sadrži samo cifre!", parent=self.view.prozor_nabavka)

    def provera_da_li_je_uneto(self, za_proveru, sta_proveravamo):
        if (za_proveru == "") or (za_proveru == 0):
            if sta_proveravamo == "inventarni broj":
                messagebox.showinfo("Greška", "Niste uneli inventarni broj", parent=self.view.prozor_nabavka)
            elif sta_proveravamo == "dobavljac":
                messagebox.showinfo("Greška", "Niste izabrali dobavljača", parent=self.view.master)
            elif sta_proveravamo == "status":
                messagebox.showinfo("Greška", "Niste izabrali status", parent=self.view.prozor_nabavka)
            elif sta_proveravamo == "nabavna":
                messagebox.showinfo("Greška", "Niste uneli nabavnu vrednost", parent=self.view.prozor_nabavka)
            elif sta_proveravamo == "naziv":
                messagebox.showinfo("Greška", "Niste uneli naziv osnovnog sredstva", parent=self.view.prozor_nabavka)
            elif sta_proveravamo == "konto":
                messagebox.showinfo("Greška", "Niste uneli konto", parent=self.view.prozor_nabavka)
            elif sta_proveravamo == "stopa":
                messagebox.showinfo("Greška", "Niste uneli amortizacionu stopu", parent=self.view.prozor_nabavka)
            elif sta_proveravamo == "dokument":
                messagebox.showinfo("Greška", "Niste uneli broj dokumenta", parent=self.view.master)
            else:
                pass
            return False
        else:
            return True

    def podaci_za_nalog_nabavke(self, id_fakture):
        unos_model = NalogUnosModel()
        return unos_model.find_nalog(id_fakture)

    def kreiraj_nalog_nabavke(self):
        ''' PROVERA DA LI POSTOJI URADJENA AMORTIZACIJA POSLE DATUMA NABAVKE OSNOVNOG SREDSTVA '''
        datum_nab = self.view.datum_nabavke.get_date()
        datum_nabavke = datum_nab.strftime('%Y-%m-%d')
        provera_amortizacija_postoji = self.postoji_amortizacija_posle_datuma(datum_nabavke)
        id_dobavljaca = self.dobijanje_id_dobavljaca()
        provera_dobavljac = self.provera_da_li_je_uneto(id_dobavljaca, "dobavljac")
        broj_dokumenta = self.view.broj_fakture.get()
        provera_dokument = self.provera_da_li_je_uneto(broj_dokumenta, "dokument")
        danasnji_datum = date.today()
        datum_kreiranja_sistemski = danasnji_datum.strftime('%Y-%m-%d')
        if provera_amortizacija_postoji:
            messagebox.showinfo("Obaveštenje", "Postoji amortizacija posle datuma nabavke, ne mozete uneti osnovno sredstvo", parent=self.view.master)
        else:
            if (provera_dokument and provera_dobavljac) is False:
                messagebox.showinfo("Obaveštenje", "Nije kreiran nalog za nabavku osnovnog sredstva", parent=self.view.master)
            else:
                try:
                    ''' unose se podaci u tabelu nabavka '''
                    unos_model = NalogUnosModel()
                    unos_model.insert_unos(id_dobavljaca, broj_dokumenta, datum_nabavke, datum_kreiranja_sistemski)
                    ''' pronadji u tabeli nabavka podatke za prikaz u prozoru nabavke '''
                    ovaj_nalog = unos_model.pronadji_poslednji()
                    id_naloga = ovaj_nalog[0][0]

                    ''' sada treba da se otvori prozor za unos nabavke opreme '''
                    self.view.otvori_prozor_nabavke(id_naloga)
                    self.view.broj_fakture.delete(0, 'end')
                    self.sve_nabavke()

                except Error as e:
                    Greske("Problem kreiranja naloga nabavke - UnosController-kreiraj_nalog_nabavke", e)
                    messagebox.showwarning("Hmmmmmmmmmm", "Nešto nije u redu!", parent=self.view.master)

    def obrisi_fakturu(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_pregled_nabavki.focus()
        if selected:
            ''' proveri da li je faktura proknjizena, ako jeste ne moze se brisati '''
            unos_model = NalogUnosModel()
            pronadjen = unos_model.find_nalog(selected)
            if pronadjen[0][2] == 1:
                messagebox.showinfo("Greska", "Ne možete da obrišete proknjižen dokument!!", parent=self.view.master)
            else:
                '''pitanje da li ste sigurni'''
                self.view.prozor_za_brisanje(selected)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedan dokument!!", parent=self.view.master)

    def obrisi_ulaznu_fakturu(self, id_fakture):
        '''Prvo proveri da li ima opreme u njemu, pa obrisi opremu iz fakture'''
        os_model = OsnovnoSredstvoModel()
        pronadjen_os = os_model.pronadji_osnovno_sredstvo_iz_fakture(id_fakture)
        unos_model = NalogUnosModel()
        if pronadjen_os:
            ''' obrisati sva osnovna sredstva iz te fakture, pa onda obrisati i fakturu'''
            for osnovno_sredstvo in pronadjen_os:
                os_model.delete_osnovno_sredstvo(osnovno_sredstvo[0])
            unos_model.delete_nalog(id_fakture)
        else:
            ''' obrisati samo fakturu nabavke'''
            unos_model.delete_nalog(id_fakture)
        # skloniti dijalog box - Da li zelite da obrisete rashod 
        self.view.prozor_brisanje.destroy()
        self.sve_nabavke()

    def prikazi_opremu_tabela_nabavke(self, id_fakture):
        # Brisanje tabele zbog popunjavanja tabele podacima iza baze - sve stavke naloga za taj nalog
        self.view.tree_tabela_nabavka.delete(*self.view.tree_tabela_nabavka.get_children())
        # pronalazenje u bazi svih ulaznih faktura
        oprema_model = OsnovnoSredstvoModel()
        data = oprema_model.pronadji_opremu_faktura_unos(id_fakture)
        self.view.tree_tabela_nabavka.tag_configure('oddrow', background="white")
        self.view.tree_tabela_nabavka.tag_configure('evenrow', background="lightblue")
        self.view.tree_tabela_nabavka.tag_configure('ukupnorow', background="#5887C2", foreground="white", font=('Helvetica', 10, 'bold'))

        ukupno_nabavna = 0
        ukupno_otpisana = 0
        count_oprema = 1
        for record in data:
            ukupno_nabavna += record[3]
            ukupno_otpisana += record[4]
            if count_oprema % 2 == 0:
                self.view.tree_tabela_nabavka.insert(parent='', index='end', iid=record[0], text='', values=(
                        count_oprema, record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]),
                                                             tags=('evenrow',))
            else:
                self.view.tree_tabela_nabavka.insert(parent='', index='end', iid=record[0], text='', values=(
                        count_oprema, record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]),
                                                             tags=('oddrow',))

            count_oprema += 1

        self.view.tree_tabela_nabavka.insert('', 'end', values=("", "", "", ukupno_nabavna, ukupno_otpisana, "", "", "", "", ""), tags=('ukupnorow',))
        # Ova komanda pomera scroll na kraj tabele da bi se videlo koji je poslednji slog unet (dobra stvar:)
        self.view.tree_tabela_nabavka.yview_moveto(1)

    def izbor_reda(self):
        return self.view.tree_tabela_nabavka.focus()

    def izaberi_red_oprema(self, e):
        # Prvo isprazniti polja
        self.ocisti_polja_unos()
        # Uzeti identifikator reda
        selected = self.izbor_reda()
        self.view.id_izmenjene_opreme.set(selected)
        # Uzamanje vrednosti iz izabranog reda
        # Mora ovaj try exept jer selektuje i header tabele, a onda vraća grešku out of range
        try:
            values_oprema = self.view.tree_tabela_nabavka.item(selected, 'values')
            # Prikaz vrednosti u entry poljima
            #last = self.view.tree_tabela_nabavka.get_children()[-1]

            self.view.inventarni_broj_entry.insert(0, values_oprema[1])
            self.view.naziv_entry.insert(0, values_oprema[2])
            self.view.nabavna_entry.insert(0, values_oprema[3])
            self.view.otpisana_entry.insert(0, values_oprema[4])
            self.view.konto_combo.set("")
            if values_oprema[6] == '':
                self.view.konto_combo.set("")
            else:
                index_konta = self.view.spisak_konta.index(values_oprema[6])
                self.view.konto_combo.current(index_konta)
            if values_oprema[5] == '':
                self.view.status_combo.current(0)
            else:
                index_statusa = self.view.spisak_statusa.index(values_oprema[5])
                self.view.status_combo.current(index_statusa)

            self.view.stopa_label_iznos.config(text=values_oprema[7])
            '''ovde setovati id stope da bi mogao da se uzme kada se radi izmena reda odnosno opreme '''
            if values_oprema[7] == '':
                self.view.id_izabrane_stope.set("")
                self.view.stopa_label_iznos.config(text='')
            else:
                self.view.stopa_label_iznos.config(text=values_oprema[7])
                os_model = OsnovnoSredstvoModel()
                pronadjen = os_model.pronadji_os_po_id(selected)
                if pronadjen[0][7] == '':
                    self.view.id_izabrane_stope.set("")
                else:
                    self.view.id_izabrane_stope.set(pronadjen[0][7])
            if values_oprema[9] == '':
                self.view.izabrana_lokacija.current(0)
            else:
                index_lokacije = self.view.spisak_lokacija.index(values_oprema[9])
                self.view.izabrana_lokacija.current(index_lokacije)
            if values_oprema[8] == '':
                self.view.zaduzenje_combo.current(0)
            else:
                index_zaduzenja = self.view.spisak_zaposlenih.index(values_oprema[8])
                self.view.zaduzenje_combo.current(index_zaduzenja)

        except IndexError:
            pass

    ''' Izmena podataka o osnovnom sredstvu u fakturi '''
    def izmeni_red(self):
        #id_selektovana_oprema = self.view.id_izmenjene_opreme.get()

        try:
            id_selektovana_oprema = self.view.id_izmenjene_opreme.get()
            #id_selektovana_oprema:
            '''uzeti sve vrednosti iz input polja i azurirati osnovno sredstvo'''
            ''' OSTALE PROVERE '''
            inv_broj = self.view.inventarni_broj_entry.get()
            if inv_broj.isnumeric():
                provera_broj = self.provera_da_li_je_uneto(inv_broj, "inventarni broj")
                naziv = self.view.naziv_entry.get()
                provera_naziv = self.provera_da_li_je_uneto(naziv, "naziv")
                nabavna = self.view.nabavna_entry.get()
                provera_nabavna = self.provera_da_li_je_uneto(nabavna, "nabavna")
                nab = nabavna.replace(",", ".")
                if nab == '0.00' or nab == '0' or nab == "":
                    nabavna_vrednost = float(0)
                else:
                    nabavna_vrednost = float(nab)
                otpis = self.view.otpisana_entry.get()
                otpis_vrednost = otpis.replace(",", ".")
                if otpis_vrednost == '0.00' or otpis_vrednost == '0' or otpis_vrednost == "":
                    otpisana_vrednost = float(0)
                else:
                    otpisana_vrednost = float(otpis_vrednost)
                id_konta = self.dobijanje_id_konta()
                provera_konta = self.provera_da_li_je_uneto(id_konta, "konto")
                status = self.view.status_combo.get()
                provera_status = self.provera_da_li_je_uneto(status, "status")

                '''pronaci id stope od izabranog osnovnog sredstva i upisati taj id '''
                stopa = self.view.id_izabrane_stope.get()

                id_lokacije = self.dobijanje_id_lokacije()
                zaposleni = self.dobijanje_id_zaposlenog()
                id_fakture = self.view.faktura
                aktiviran = 0
                if (provera_broj and provera_status and provera_naziv and provera_konta and provera_nabavna) is False:
                    messagebox.showinfo("Obaveštenje", "Osnovno sredstvo nije uneto", parent=self.view.prozor_nabavka)
                else:
                    try:
                        model = OsnovnoSredstvoModel()
                        '''ovde se proverava da li u tabeli postoji inventarni broj - ako korisnik izmeni inventarni broj koji je selektovao '''
                        pronadjen_inv_broj = model.postoji_inv_broj_osim_selektovanog(id_selektovana_oprema, inv_broj)
                        if not pronadjen_inv_broj:
                            ''' knjizenje - izmena osnovnog sredstva'''
                            model.izmena_novog_osnovnog_sredstva(id_selektovana_oprema, int(inv_broj), naziv, nabavna_vrednost, otpisana_vrednost, status,
                                                               id_konta, stopa, zaposleni, id_lokacije, id_fakture, aktiviran)
                            self.ocisti_polja_unos()
                            self.prikazi_opremu_tabela_nabavke(id_fakture)
                            self.view.inventarni_broj_entry.focus()
                        else:
                            messagebox.showwarning("Greška", "Već postoji takav inventarni broj u bazi!", parent=self.view.prozor_nabavka)
                    except Error as e:
                        Greske("Problem izmena osnovnog sredstva u bazu - OsnovnoSredstvoModel-izmena_novog_osnovnog_sredstva", e)
                        messagebox.showwarning("Hmmmmmmmmmm", "Nešto nije u redu!", parent=self.view.prozor_nabavka)
            else:
                messagebox.showwarning("Greška", "Inventarni broj može da sadrži samo cifre!", parent=self.view.prozor_nabavka)
        except:
            messagebox.showwarning("Hmmmmmmmmmm", "Niste izabrali ni jedno osnovno sredstvo!", parent=self.view.prozor_nabavka)

    ''' Brisanje reda - osnovnog sredstva iz ulazne fakture '''
    def obrisi_red(self):
        # Uzeti identifikator reda
        selected = self.view.tree_tabela_nabavka.focus()
        if selected:
            id_fakture = self.view.faktura
            oprema_model = OsnovnoSredstvoModel()
            oprema_model.delete_osnovno_sredstvo(selected)
            self.prikazi_opremu_tabela_nabavke(id_fakture)
            self.ocisti_polja_unos()
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedno osnovno sredstvo!!", parent=self.view.prozor_nabavka)

    def proknjizi_fakturu(self):
        id_fakture = self.view.faktura
        ''' prvo proveriti da li faktura ima stavke, ako nema, ne moze da se proknjizi'''
        os_model = OsnovnoSredstvoModel()
        pronadjena_oprema = os_model.pronadji_osnovno_sredstvo_iz_fakture(id_fakture)

        if pronadjena_oprema:
            ''' azuriraj nabavku tako sto se promeni proknjizen u 1'''
            unos_model = NalogUnosModel()
            unos_model.proknjizi_nabavku(id_fakture)
            ''' azuriraj osnovno sredstvo tako sto se promeni aktiviran u 1 '''
            ''' prvo pronaci sva osnovna sredstva koja se nalaze u fakturi, a onda ih azurirati '''

            pronadjena_oprema = os_model.pronadji_osnovno_sredstvo_iz_fakture(id_fakture)
            for oprema in pronadjena_oprema:
                os_model.aktiviraj_os(oprema[0])
            ''' na kraju dugmad dodaj, izmeni, obrisi i proknjizi da budu read only'''
            self.view.proknjizen_da_ne.config(text="Da")
            self.view.dugme_dodaj.config(state="disabled")
            self.view.dugme_izmeni.config(state="disabled")
            self.view.dugme_obrisi.config(state="disabled")
            self.view.dugme_proknjizi.config(state="disabled")
            self.view.dugme_stampaj.config(state="normal")
            messagebox.showinfo("Uspešno", "Proknjižili ste dokument!!", parent=self.view.prozor_nabavka)
            self.sve_nabavke()

        else:
            messagebox.showinfo("Hmmmmmmm", "Ne možete proknjižiti praznu fakturu!!", parent=self.view.prozor_nabavka)

    def stampa_fakture(self):
        id_fakture = self.view.faktura
        ''' pronadji detalje ulaznog dokumenta'''
        nalog_model = NalogUnosModel()
        pronadjena_faktura = nalog_model.find_nalog(id_fakture)
        ''' pronadji sva osnovna sredstva koja se nalaze u ulaznoj fakturi'''
        os_model = OsnovnoSredstvoModel()
        pronadjena_oprema = os_model.pronadji_osnovno_sredstvo_iz_fakture(id_fakture)
        ''' uraditi rekapitulaciju po kontima group by konto_id'''
        rekapitulacija_po_kontima = os_model.pronadji_osnovno_sredstvo_iz_fakture_po_kontima(id_fakture)
        try:
            stampanje = StampaIzvestaja()
            stampanje.stampa_ulazne_fakture(pronadjena_faktura, pronadjena_oprema, rekapitulacija_po_kontima)
        except OSError:
            messagebox.showwarning("Greška", "Već imate otvorenu ulaznu fakturu u PDF-u. Morate je prvo zatvoriti da bi ste odštampali novu!", parent=self.view.prozor_nabavka)

    # Smanjivanje liste konta u comboboxu na osnovu onoga sto kuca korisnik
    '''
    def check_input(self, event):
        value = event.widget.get()
        if value == '':
            self.view.unet_naziv_dobavljaca['values'] = self.view.lista_dobavljaca
        else:
            data = []
            for item in self.view.unet_naziv_dobavljaca:
                if value.lower() in item.lower():
                    data.append(item)

            self.view.unet_naziv_dobavljaca['values'] = data
    '''




