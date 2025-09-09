from models.amortizacija_model import AmortizacijaModel
from datetime import datetime, date
from models.osnovno_sredstvo_model import OsnovnoSredstvoModel
from models.rashod_model import RashodModel
from views.stampa_izvestaja import StampaIzvestaja
from tkinter import messagebox
import xlsxwriter
import os


class ListeController:
    def __init__(self, view):
        self.view = view

    ''' Pokretanje otvaranja prozora za pregled amortizacije '''

    def start(self):
        self.view.pokreni(self)

    @staticmethod
    def lista_svih_datuma():
        amortizacija_model = AmortizacijaModel()
        amortizacije = amortizacija_model.pronadji_sve_uradjene_amortizacije()
        amortizacije_lista = []
        for i in amortizacije:
            amortizacije_lista.append(i[1].strftime('%d.%m.%Y.'))
        amortizacije_lista.append("Na današnji dan")
        return amortizacije_lista

    @staticmethod
    def nadji_id_amortizacije(datum):
        am_model = AmortizacijaModel()
        return am_model.pronadji_amortizaciju_po_datumu(datum)[0][0]

    def koju_listu_stampam(self, sort, rez, datum):
        stampa = StampaIzvestaja()
        if sort == "inventarni_broj":
            stampa.stampa_popisne_liste_za_popisivanje(rez, datum)
        else:
            stampa.stampa_popisne_liste_sortirano(rez, datum)

    def stampa_popisne_liste(self):
        try:
            datum = self.view.padajuca_lista_datuma.get()
            sort = self.view.padajuca_lista_sortirano.get()
            if sort == "po inventarnom broju":
                sortiranje = "inventarni_broj"
            elif sort == "po korisnicima":
                sortiranje = "zaposleni_id"
            elif sort == "po kancelarijama":
                sortiranje = "lokacija_id"
            else:
                sortiranje = "stopa_id"

            os_model = OsnovnoSredstvoModel()
            stampa = StampaIzvestaja()
            if datum == "Na današnji dan":
                datum_popisne = date.today()
                datum_popisne_liste = datum_popisne.strftime("%d.%m.%Y.")
                rezultat = os_model.osnovna_sredstva_aktivna_amortizovana_danas(sortiranje)
                if sortiranje == "inventarni_broj":
                    #rezultat = os_model.osnovna_sredstva_aktivna_amortizovana_danas(sortiranje)
                    stampa.stampa_popisne_liste_za_popisivanje(rezultat, datum_popisne_liste)
                elif sortiranje == "zaposleni_id":
                    stampa.stampa_popisne_liste_sortirano(rezultat, datum_popisne_liste)
                elif sortiranje == "lokacija_id":
                    stampa.stampa_popisne_liste_po_kancelarijama(rezultat, datum_popisne_liste)
                else:
                    rezultat_amort_grupe = os_model.osnovna_sredstva_aktivna_amortizovana_danas_amortizacione_grupe(sortiranje)
                    stampa.stampa_popisne_liste_po_amortizacionim_grupama(rezultat_amort_grupe, datum_popisne_liste)

            else:
                datum_formirano = datetime.strptime(datum, '%d.%m.%Y.').date()
                id_amortizacije = self.nadji_id_amortizacije(datum_formirano)
                datum_popisne_liste = datum
                rezultat = os_model.popisna_lista_po_datumu_amortizacije(id_amortizacije, sortiranje)
                if sortiranje == "inventarni_broj":
                    stampa.stampa_popisne_liste_za_popisivanje(rezultat, datum_popisne_liste)
                elif sortiranje == "zaposleni_id":
                    stampa.stampa_popisne_liste_sortirano(rezultat, datum_popisne_liste)
                elif sortiranje == 'lokacija_id':
                    stampa.stampa_popisne_liste_po_kancelarijama(rezultat, datum_popisne_liste)
                else:
                    rezultat_amort_grupe = os_model.popisna_lista_po_datumu_amortizacije_amortiz_grupe(id_amortizacije, sortiranje)
                    stampa.stampa_popisne_liste_po_amortizacionim_grupama(rezultat_amort_grupe, datum_popisne_liste)
        except OSError:
            messagebox.showwarning("Greška", "Već imate otvorenu popisnu listu u PDF-u. Morate prvo zatvoriti prethodni izveštaj!", parent=self.view.liste_frame)

    def stampa_ostalo(self):
        try:
            koja_lista = self.view.vrste_kombo.get()
            pocetni_datum = self.view.datum_od.get_date()
            krajnji_datum = self.view.datum_do.get_date()
            os_model = OsnovnoSredstvoModel()
            stampa = StampaIzvestaja()
            if koja_lista == "Nabavljene opreme":
                rezultat = os_model.nabavljena_oprema_po_datumu(pocetni_datum, krajnji_datum)
                stampa.stampa_popisa_nabavljene_opreme(rezultat, pocetni_datum, krajnji_datum)
            else:
                rezultat = os_model.rashodovana_oprema_po_datumu(pocetni_datum, krajnji_datum)
                stampa.stampa_popisa_rashodovane_opreme(rezultat, pocetni_datum, krajnji_datum)
        except OSError:
            messagebox.showwarning("Greška", "Već imate otvorenu listu u PDF-u. Morate prvo zatvoriti prethodni izveštaj!", parent=self.view.liste_frame)

    # Funkcija za eksport pomocne knjige osnovnih sredstava u excel
    def eksportovanje(self):
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook('pomocna_knjiga_os.xlsx')
        worksheet = workbook.add_worksheet()
        # Add a bold format to use to highlight cells.
        cell_format = workbook.add_format({'valign': 'center', 'border': 1})
        cell_format.set_text_wrap()
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells
        # money = workbook.add_format({'num_format': '#,##0.00'})
        zaglavlje = workbook.add_format({'valign': 'center'})
        zaglavlje_datum = workbook.add_format({'valign': 'center', 'num_format': 'dd.mm.yyyy.'})
        zaglavlje_novac = workbook.add_format({'valign': 'center', 'num_format': '#,##0.00'})
        naslov = workbook.add_format({'valign': 'center', 'font': {'name': 'Arial', 'size': 16}, 'bold': True})
        zaglavlje_tabele_brojevi = workbook.add_format({'valign': 'center', 'border': 1})
        # tabela_cell_format
        tabela_money = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        tabela_datum = workbook.add_format({'valign': 'center', 'num_format': 'dd.mm.yyyy.', 'border': 1})
        # bold_money = workbook.add_format({'num_format': '#,##0.00', 'bold': True})
        # format_datuma = workbook.add_format({'num_format': 'dd.mm.yyyy.'})

        os_model = OsnovnoSredstvoModel()
        rezultat = os_model.sva_oprema_knjiga_os()
        am_model = AmortizacijaModel()
        rashod_model = RashodModel()
        row = 0
        col = 0

        for idos, invbroj, naziv, nabavna, otpisana, grupa, stopa, datum, broj_fakture in rezultat:
            # Write some data headers.
            godisnja_stopa = str(stopa) + "%"
            neotpisana_vrednost = nabavna - otpisana
            worksheet.write(row, col, 'Inventarski broj:', bold)
            worksheet.write(row + 1, col, 'Naziv osnovnog sredstva:', bold)
            worksheet.write(row + 2, col, 'Amortizaciona grupa:', bold)
            worksheet.write(row + 3, col, 'Godišnja stopa:', bold)
            worksheet.write(row + 4, col, 'Metod amortizacije:', bold)
            worksheet.write(row + 5, col, 'Datum nabavke:', bold)
            worksheet.write(row + 6, col, 'Nabavna vrednost:', bold)

            worksheet.write(row, col + 1, invbroj, zaglavlje)
            worksheet.write(row + 1, col + 1, naziv, zaglavlje)
            worksheet.write(row + 2, col + 1, grupa, zaglavlje)
            worksheet.write(row + 3, col + 1, godisnja_stopa, zaglavlje)
            worksheet.write(row + 4, col + 1, 'Proporcionalni', zaglavlje)
            worksheet.write(row + 5, col + 1, datum, zaglavlje_datum)
            worksheet.write(row + 6, col + 1, nabavna, zaglavlje_novac)

            worksheet.merge_range(row + 8, col + 2, row + 8, col + 7, 'Knjiga osnovnih sredstava i sitnog inventara',
                                  naslov)
            # Pravljenje zaglavlja tabele
            worksheet.write(row + 10, col, 'Datum knjizenja', cell_format)
            worksheet.write(row + 10, col + 1, 'Redni broj \n iz poslovne knjige \n PK-1', cell_format)
            worksheet.write(row + 10, col + 2, 'Opis \n (naziv, broj i datum)', cell_format)
            worksheet.write(row + 10, col + 3, 'Nabavna vrednost \n na dan 01.01. ili \n na dan nabavke', cell_format)
            worksheet.write(row + 10, col + 4, 'Ispravka vrednosti \n na dan 01.01. ili \n na dan nabavke', cell_format)
            worksheet.write(row + 10, col + 5, 'Neotpisana vrednost \n na dan 01.01. ili \n na dan nabavke',
                            cell_format)
            worksheet.write(row + 10, col + 6, 'Osnovica \n za amortizaciju', cell_format)
            worksheet.write(row + 10, col + 7, 'Amortizacija', cell_format)
            worksheet.write(row + 10, col + 8, 'Neotpisana vrednost \n na dan 31.12. ili \n dan otuđenja', cell_format)
            worksheet.write(row + 10, col + 9, 'Vrednost \n postignuta prodajom', cell_format)
            worksheet.write(row + 10, col + 10, 'Rashodovana \n vrednost (10-9)', cell_format)
            # U ovom redu se samo ispisuje redni brojevi od 1 do 11
            worksheet.write(row + 11, col, 1, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 1, 2, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 2, 3, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 3, 4, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 4, 5, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 5, 6, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 6, 7, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 7, 8, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 8, 9, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 9, 10, zaglavlje_tabele_brojevi)
            worksheet.write(row + 11, col + 10, 11, zaglavlje_tabele_brojevi)
            # Prvi red ispisuje se nabavka osnovnog sredstva
            if neotpisana_vrednost > 0:
                osnovica_za_amortizaciju = nabavna
            else:
                osnovica_za_amortizaciju = 0
            worksheet.write(row + 12, col, datum, tabela_datum)
            worksheet.write(row + 12, col + 1, '', cell_format)
            worksheet.write(row + 12, col + 2, 'Nabavka: ' + broj_fakture, cell_format)
            worksheet.write(row + 12, col + 3, nabavna, tabela_money)
            worksheet.write(row + 12, col + 4, otpisana, tabela_money)
            worksheet.write(row + 12, col + 5, neotpisana_vrednost, tabela_money)
            worksheet.write(row + 12, col + 6, osnovica_za_amortizaciju, tabela_money)
            worksheet.write(row + 12, col + 7, '', cell_format)
            worksheet.write(row + 12, col + 8, neotpisana_vrednost, tabela_money)
            worksheet.write(row + 12, col + 9, '', tabela_money)
            worksheet.write(row + 12, col + 10, '', tabela_money)

            # FOR petlja za svako osnovno sredstvo izlistaju se sve amortizacije i ispisu se u excelu
            spisak_amortizacija = am_model.pronadji_amortizaciju_za_os(idos)
            redovi = 13
            for id_os, datum_amortizacije, broj_amortizacije, nabavna_vrednost, otpisana_vrednost, tekuca_amortizacija in spisak_amortizacija:
                # print(tekuca_amortizacija)
                if tekuca_amortizacija > 0:
                    preostala_vrednost = nabavna_vrednost - otpisana_vrednost
                    nova_neotpisana_vrednost = preostala_vrednost - tekuca_amortizacija
                    # Ovde se ispisuju amortizacije za svako osnovno sredstvo
                    worksheet.write(row + redovi, col, datum_amortizacije, tabela_datum)
                    worksheet.write(row + redovi, col + 1, ' ', cell_format)
                    worksheet.write(row + redovi, col + 2, broj_amortizacije, cell_format)
                    worksheet.write(row + redovi, col + 3, nabavna_vrednost, tabela_money)
                    worksheet.write(row + redovi, col + 4, otpisana_vrednost, tabela_money)
                    worksheet.write(row + redovi, col + 5, preostala_vrednost, tabela_money)
                    worksheet.write(row + redovi, col + 6, nabavna_vrednost, tabela_money)
                    worksheet.write(row + redovi, col + 7, tekuca_amortizacija, tabela_money)
                    worksheet.write(row + redovi, col + 8, nova_neotpisana_vrednost, tabela_money)
                    worksheet.write(row + redovi, col + 9, '', tabela_money)
                    worksheet.write(row + redovi, col + 10, '', tabela_money)
                    redovi += 1

            # FOR petlja za ispis rashoda
            spisak_rashoda = rashod_model.trazenje_rashoda_po_os(idos)
            if spisak_rashoda:
                for id_osn, datum_rashoda, broj_rashoda, nabavna_vrednost_rashod, otpisana_vrednost_rashod, amortizacija_r in spisak_rashoda:
                    # Ovde se ispisuju amortizacije za svako osnovno sredstvo
                    preostala_vrednost_rashod = nabavna_vrednost_rashod - otpisana_vrednost_rashod
                    nova_neotpisana_vrednost_rashod = preostala_vrednost_rashod - amortizacija_r
                    if preostala_vrednost_rashod > 0:
                        osnovica_za_amortizaciju_rashod = nabavna_vrednost_rashod
                    else:
                        osnovica_za_amortizaciju_rashod = 0
                    worksheet.write(row + redovi, col, datum_rashoda, tabela_datum)
                    worksheet.write(row + redovi, col + 1, ' ', cell_format)
                    worksheet.write(row + redovi, col + 2, 'Rashod: ' + broj_rashoda, cell_format)
                    worksheet.write(row + redovi, col + 3, nabavna_vrednost_rashod, tabela_money)
                    worksheet.write(row + redovi, col + 4, otpisana_vrednost_rashod, tabela_money)
                    worksheet.write(row + redovi, col + 5, preostala_vrednost_rashod, tabela_money)
                    worksheet.write(row + redovi, col + 6, osnovica_za_amortizaciju_rashod, tabela_money)
                    worksheet.write(row + redovi, col + 7, amortizacija_r, tabela_money)
                    worksheet.write(row + redovi, col + 8, nova_neotpisana_vrednost_rashod, tabela_money)
                    worksheet.write(row + redovi, col + 9, '', tabela_money)
                    worksheet.write(row + redovi, col + 10, '', tabela_money)
                    redovi += 1

            row += 12 + redovi

        # Autofit the worksheet.
        worksheet.autofit()
        workbook.close()
        os.startfile('pomocna_knjiga_os.xlsx')

    def pomocna_knjiga_os(self):
        # Prvo se izlistaju sva osnovna sredstva
        try:
            self.eksportovanje()
        except:
            messagebox.showwarning("Greška", "Nesto nije u redu sa formiranjem izvestaja! Verovatno već imate otvorenu pomoćnu knjigu! Poverite!", parent=self.view.liste_frame)


