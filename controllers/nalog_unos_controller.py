from tkinter import messagebox
from models.dobavljaci_model import DobavljaciModel
from datetime import datetime


class NalogUnosController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        self.view.pokreni(self)

    @staticmethod
    def lista_dobavljaca():
        dobavljaci = DobavljaciModel()
        svi_dobavljaci = dobavljaci.read()
        dobavljaci_i_id = {}
        for record in svi_dobavljaci:
            dobavljaci_i_id.update({record[0]: record[1]})

        return dobavljaci_i_id

    ''' Pretvara datume koji su izabrani na ekranu u datatype object za unos u bazu'''
    @staticmethod
    def konvertuj_u_datum(izabran_datum):
        return datetime.strptime(izabran_datum, "%d.%m.%Y").strftime("%Y-%m-%d")

    ''' Na osnovu naziv dobavljaca dobija se njegov id za unos u bazu '''
    def pronadji_id_dobavljaca(self, naziv) -> int:
        return list(self.lista_dobavljaca().keys())[list(self.lista_dobavljaca().values()).index(naziv)]

    def ocisti_polja(self) -> None:
        self.view.broj_naloga.delete(0, 'end')
        self.view.entry_broj_fakture.delete(0, 'end')

    '''Ovo ide u prozor kada se otvori nalog da se ispisu broj naloga, datum naloga i da li je proknjizen'''
    def pronadji_nalog(self, idnaloga):
        '''find nalog'''
        rezultat = self.model.find_nalog(idnaloga)
        return rezultat

    ''' Unos naloga za unos os '''
    def unos_naloga(self):
        broj_naloga = self.view.broj_naloga.get()
        datum_naloga = self.view.datum_novog_naloga.get()
        dobavljac = self.view.dobavljac_entry.get()
        broj_fakture = self.view.entry_broj_fakture.get()
        datum_fakture = self.view.datum_fakture.get()

        ''' Unos naloga u bazu podataka'''
        if broj_naloga == '' or dobavljac == '' or broj_fakture == '':
            messagebox.showwarning("Greška", "Morate popuniti sva polja!", parent=self.view.master)
        else:
            id_dobavljaca = self.pronadji_id_dobavljaca(dobavljac)
            datum_naloga_baza = self.konvertuj_u_datum(datum_naloga)
            datum_fakture_baza = self.konvertuj_u_datum(datum_fakture)
            self.model.insert_unos(broj_naloga, datum_naloga_baza, id_dobavljaca, broj_fakture, datum_fakture_baza)
            # Brisanje entry polja nakon unosa konta
            self.ocisti_polja()
            # Pronaci ovaj nalog
            novi_nalog = self.model.pronadji_poslednji()
            id_novog_naloga = novi_nalog[0][0]
            rezultat = self.pronadji_nalog(id_novog_naloga)
            ''' Otvara prozor za unos osnovnih sredstava - nalazi se u view folderu'''
            self.view.kreiraj_unos(self, id_novog_naloga, rezultat[0][1], rezultat[0][2], rezultat[0][3], rezultat[0][5], rezultat[0][6])
