import locale
from models.osnovno_sredstvo_model import OsnovnoSredstvoModel
from models.mesta_model import MestaModel
from models.dobavljaci_model import DobavljaciModel
from models.konto_model import KontoModel
from models.stope_model import StopeModel
from models.korisnici_model import KorisniciModel
from mysql.connector import Error
from views.greske import Greske
from tkinter import messagebox


class NaslovnaListaController:
    def __init__(self, view):
        self.view = view

    def start(self):
        self.view.pokreni(self)

    @staticmethod
    def ucitaj_os_model():
        return OsnovnoSredstvoModel()

    @staticmethod
    def dobijanje_id_inv_broja(inv_broj):
        os_model = OsnovnoSredstvoModel()
        return os_model.pronadji_osnovno_sredstvo_inv_broj(inv_broj)

    @staticmethod
    def pronadji_id_stope_inv_broj(inventarni_broj):
        os_model = OsnovnoSredstvoModel()
        pronadji = os_model.pronadji_id_stope(inventarni_broj)
        return pronadji[0][0]

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
        izabrana_vrednost = self.view.unet_naziv_dobavljaca_izmena.get()
        id_dobavljaca = [k for k, v in dictionary_dobavljaca.items() if v == izabrana_vrednost]
        if not id_dobavljaca:
            return ""
        else:
            return id_dobavljaca[0]

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
        izabrana_vrednost = self.view.unet_konto_izmena.get()
        id_konta = [k for k, v in dictionary_konta.items() if v == izabrana_vrednost]
        if not id_konta:
            return ""
        else:
            return id_konta[0]

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
            self.view.izabrana_stopa_izmena.config(text=izabrana_stopa[0][0])
            self.view.id_izabrane_stope.set(selected)
            self.view.prozor_izbor_stope.destroy()
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednu stopu!!", parent=self.view.prozor_izbor_stope)

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
        izabrana_vrednost = self.view.prikazi_lokacija.get()
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
        izabrana_vrednost = self.view.prikazi_zaduzenje.get()
        id_zaposlenog = [k for k, v in dictionary_zaposleni.items() if v == izabrana_vrednost]
        if not id_zaposlenog:
            return ""
        else:
            return id_zaposlenog[0]

    ''' Ucitavanje liste mesta u prozoru za unos osnovnog sredstva '''
    @staticmethod
    def pronadji_mesta():
        mesto = MestaModel()
        rezultat = mesto.read()
        lista = []
        for oznaka in rezultat:
            lista.append(oznaka[1])
        return lista

    def provera_da_li_je_uneto(self, za_proveru, sta_proveravamo):
        if (za_proveru == "") or (za_proveru == 0):
            if sta_proveravamo == "inventarni broj":
                messagebox.showinfo("Greška", "Niste uneli inventarni broj", parent=self.view.master)
            elif sta_proveravamo == "dobavljac":
                messagebox.showinfo("Greška", "Niste izabrali dobavljača", parent=self.view.master)
            elif sta_proveravamo == "status":
                messagebox.showinfo("Greška", "Niste izabrali status", parent=self.view.master)
            elif sta_proveravamo == "naziv":
                messagebox.showinfo("Greška", "Niste uneli naziv osnovnog sredstva", parent=self.view.master)
            elif sta_proveravamo == "konto":
                messagebox.showinfo("Greška", "Niste uneli konto", parent=self.view.master)
            elif sta_proveravamo == "stopa":
                messagebox.showinfo("Greška", "Niste uneli amortizacionu stopu", parent=self.view.master)
            else:
                pass
            return False
        else:
            return True

    def izmeni_osnovno_sredstvo(self):
        inv_broj = self.view.prikazi_inventarni_broj.cget("text")
        if not inv_broj:
            messagebox.showwarning("Hmmmmmmmmmm", "Niste izabrali ni jedno osnovno sredstvo!", parent=self.view.pregled_opreme)
        else:
            id_lokacije = self.dobijanje_id_lokacije()
            zaposleni = self.dobijanje_id_zaposlenog()
            try:
                model = OsnovnoSredstvoModel()
                pronadji_osnovno_sredstvo = model.postoji_osnovno_sredstvo(inv_broj)
                id_os = pronadji_osnovno_sredstvo[0][0]
                model.update_osnovno_sredstvo(id_os, id_lokacije, zaposleni)
                messagebox.showinfo("Obaveštenje", "Uspešno ste izmenili osnovno sredstvo", parent=self.view.pregled_opreme)
            except Error as e:
                Greske("Problem izmene osnovnog sredstva - OsnovnoSredstvoModel-izmena_osnovnog_sredstva", e)
                messagebox.showwarning("Hmmmmmmmmmm", "Nešto nije u redu!", parent=self.view.prozor_izmena)

    def pregledaj_detalje_os(self, e=None):
        id_opreme = self.view.my_tree.focus()
        mod = self.ucitaj_os_model()
        nadji = mod.pronadji_osnovno_sredstvo(id_opreme)
        if not nadji:
            messagebox.showwarning("Hmmmmm", "Niste izabrali ni jedno osnovno sredstvo!",
                                   parent=self.view.master)
        else:
            self.view.prikazi_inventarni_broj.config(text=nadji[0][1])
            self.view.prikazi_naziv.config(text=nadji[0][2])
            self.view.prikazi_datum_nabavke.config(text=nadji[0][3].strftime("%d.%m.%Y"))
            self.view.prikazi_broj_fakture.config(text=nadji[0][4])
            self.view.prikazi_naziv_dobavljaca.config(text=nadji[0][5])

            nabavna_vrednost_prikaz = locale.format_string('%10.2f', nadji[0][6], grouping=True)
            otpisana_vrednost_prikaz = locale.format_string('%10.2f', nadji[0][7], grouping=True)
            trenutna_vrednost = nadji[0][6] - nadji[0][7]
            trenutna_vrednost_prikaz = locale.format_string('%10.2f', trenutna_vrednost, grouping=True)

            self.view.prikazi_nabavna_vrednost.config(text=nabavna_vrednost_prikaz)
            self.view.prikazi_otpisana_vrednost.config(text=otpisana_vrednost_prikaz)
            self.view.prikazi_trenutna_vrednost.config(text=trenutna_vrednost_prikaz)
            self.view.prikazi_status.config(text=nadji[0][8])
            self.view.prikazi_konto.config(text=nadji[0][9])
            self.view.prikazi_stopa.config(text=nadji[0][10])
            index_lokacije = self.view.spisak_lokacija.index(nadji[0][11])
            self.view.prikazi_lokacija.current(index_lokacije)
            index_zaduzenje = self.view.spisak_zaposlenih.index(nadji[0][12])
            self.view.prikazi_zaduzenje.current(index_zaduzenje)

    def spisak_opreme(self):
        ''' Povuci podatke iz baze '''
        nl = self.ucitaj_os_model()
        rezultat_stavke = nl.read_osnovna_sredstva_aktivna_amortizovana()
        ''' Prikazati podatke u tabeli '''
        locale.setlocale(locale.LC_ALL, 'de_DE')
        # Brisanje tabele zbog popunjavanja tabele podacima iza baze - sve stavke naloga za taj nalog

        self.view.my_tree.delete(*self.view.my_tree.get_children())
        # Pretraga baze za stavkama naloga
        # Ovde idu podaci iz stavki naloga i prikazuju se u tabeli

        self.view.my_tree.tag_configure('oddrow', background="white")
        self.view.my_tree.tag_configure('evenrow', background="lightblue")
        count_os = 1
        if not rezultat_stavke:
            pass
        else:
            for record in rezultat_stavke:
                if count_os % 2 == 0:
                    self.view.my_tree.insert(parent='', index='end', iid=record[0], text='', values=(
                        count_os, record[1], record[2], record[3].strftime('%d.%m.%Y.'),
                        locale.format_string('%10.2f', record[4], grouping=True)), tags=('evenrow',))
                else:
                    self.view.my_tree.insert(parent='', index='end', iid=record[0], text='', values=(
                        count_os, record[1], record[2], record[3].strftime('%d.%m.%Y.'),
                        locale.format_string('%10.2f', record[4], grouping=True)), tags=('oddrow',))
                count_os += 1
