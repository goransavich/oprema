from datetime import date
from tkinter import messagebox
from models.osnovno_sredstvo_model import OsnovnoSredstvoModel
from models.amortizacija_model import AmortizacijaModel
from models.stope_model import StopeModel
from views.stampa_izvestaja import StampaIzvestaja
from controllers.keyboard_controller import KeyboardController
import locale


class RashodController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    ''' Pokretanje otvaranja prozora za pregled amortizacije '''

    def start(self):
        self.view.pokreni(self)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_broj_dokumenta(self, event=None):
        if self.view.broj_dokumenta.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latiničnu tastaturu !!", parent=self.view.master)
                self.view.broj_dokumenta.delete(0, 'end')

    def pronadji_os_u_nalogu(self, id_naloga):
        os_model = OsnovnoSredstvoModel()
        return os_model.pronadji_sva_os_nalog_rashod(id_naloga)

    def nalog_list_os_za_rashod(self, id_naloga):
        # Brisanje tabele zbog azuriranja
        self.view.my_tree_rashod_tabela.delete(*self.view.my_tree_rashod_tabela.get_children())
        ''' Ovde ide upit za dobijanje spiska opreme iz tabele rashod opreme koja ima id_naloga'''
        rezultat = self.pronadji_os_u_nalogu(id_naloga)
        count_oprema = 0
        for record in rezultat:

            if count_oprema % 2 == 0:
                self.view.my_tree_rashod_tabela.insert(parent='', index='end', iid=record[0], text='',
                                                     values=(
                                                         count_oprema+1, record[1], record[2], record[3].strftime('%d.%m.%Y.')),
                                                     tags=('evenrow',))
            else:
                self.view.my_tree_rashod_tabela.insert(parent='', index='end', iid=record[0], text='',
                                                     values=(
                                                         count_oprema+1, record[1], record[2], record[3].strftime('%d.%m.%Y.')),
                                                     tags=('oddrow',))
            count_oprema += 1
        # Ova komanda pomera scroll na kraj tabele da bi se videlo koji je poslednji slog unet (dobra stvar:)
        self.view.my_tree_rashod_tabela.yview_moveto(1)

    def izracunaj_amortizovanu_vrednost(self, nabavna, procenat, broj_meseci):
        obracunata_amortizacija = nabavna*procenat/100*broj_meseci/12
        return round(obracunata_amortizacija, 2)

    def izracunaj_broj_meseci_za_amortizaciju(self, status, mesec_amortizacije, umanjenik):
        if status == 'aktivno':
            return mesec_amortizacije-umanjenik
        else:
            return 0

    def koliko_meseci(self, godina_amortizacije, godina_pretposlednje, osnovno_sredstvo, mesec_pretposlednje, mesec_amortizacije):
        if godina_amortizacije == godina_pretposlednje:
            if osnovno_sredstvo[0][10].year == godina_amortizacije:
                if osnovno_sredstvo[0][10].month > mesec_pretposlednje:
                    return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[0][5],
                                                                                      mesec_amortizacije,
                                                                                      osnovno_sredstvo[0][10].month)
                else:
                    return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[0][5],
                                                                                      mesec_amortizacije,
                                                                                      mesec_pretposlednje)
            else:
                return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[0][5],
                                                                                  mesec_amortizacije,
                                                                                  mesec_pretposlednje)
        else:
            if osnovno_sredstvo[0][10].year == godina_amortizacije:
                return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[0][5],
                                                                                  mesec_amortizacije,
                                                                                  osnovno_sredstvo[0][10].month)
            else:
                return self.izracunaj_broj_meseci_za_amortizaciju(osnovno_sredstvo[0][5],
                                                                                  mesec_amortizacije, 0)

    ''' ovde dodajem vrednost amortizacije rashoda na otpisanu vrednost os, ako je zbir ove dve vrednosti veci
        od nabavne vrednosti, onda se amortizovana umanjuje i takva se upisuje u tabelu rashod_opreme'''
    def izracunaj_amortizovanu_vrednost_final(self, nabavna, otpisana, amortizovana):
        if nabavna-otpisana < amortizovana:
            return nabavna-otpisana
        else:
            return amortizovana

    def uradi_amortizaciju_rashoda(self, osnovno_sredstvo):
        datum_amortizacije_rashoda = self.datum_rashoda()
        datum_amortizacije_rashoda_godina = datum_amortizacije_rashoda.year
        godina_amortizacije = datum_amortizacije_rashoda_godina
        mesec_amortizacije = datum_amortizacije_rashoda.month
        am_model = AmortizacijaModel()
        stope_model = StopeModel()
        procenat = stope_model.find_stopa(osnovno_sredstvo[0][7])
        poslednja_amortizacija = am_model.pronadji_poslednju_amortizaciju()
        if not poslednja_amortizacija:
            godina_pretposlednje = 0
            mesec_pretposlednje = 0
        else:
            godina_pretposlednje = poslednja_amortizacija[0][1].year
            mesec_pretposlednje = poslednja_amortizacija[0][1].month
        '''uradi amortizaciju rashoda'''
        broj_meseci = self.koliko_meseci(godina_amortizacije, godina_pretposlednje, osnovno_sredstvo, mesec_pretposlednje, mesec_amortizacije)

        vrednost_amortizacije_rashoda = self.izracunaj_amortizovanu_vrednost(osnovno_sredstvo[0][3], procenat[0][0], broj_meseci)
        ''' PRVO PROVERITI DA LI JE OTPISANA I AMORTIZOVANA VREDNOST VECA OD NABAVNE, AKO JESTE UMANJITI AMORTIZOVANU VREDNOST'''
        amortizovana_vrednost_final = self.izracunaj_amortizovanu_vrednost_final(osnovno_sredstvo[0][3], osnovno_sredstvo[0][4], vrednost_amortizacije_rashoda)
        rashod_id = self.view.rashod_id.get()
        ''' unesi podatke u tabelu u bazi rashod_opreme'''
        self.model.unesi_rashod_opreme(rashod_id, osnovno_sredstvo[0][0], float(osnovno_sredstvo[0][3]), float(osnovno_sredstvo[0][4]), float(amortizovana_vrednost_final))
        ''' Ponovo ucitaj tabelu sa spiskom opreme za taj nalog rashoda'''
        self.nalog_list_os_za_rashod(rashod_id)

    ''' Kada se klikne na dugme pronadji OS kod rashoda opreme'''
    def pronadji_os(self, e=None):
        rashod_id = self.view.rashod_id.get()
        nalog_rashoda = self.model.pronadji_nalog_rashoda(rashod_id)
        datum_rashoda = nalog_rashoda[0][1]
        inventarni_broj = self.view.unos_inventarni_broj.get()
        ''' Ovde se trazi osnovno sredstvo po inventarnom broju, da se upise u tabelu rashod opreme i izracuna amortizacija rashoda'''
        os_model = OsnovnoSredstvoModel()
        pronadjen = os_model.da_li_postoji_os(inventarni_broj)
        if pronadjen:
            ''' Provera da li je osnovno sredstvo u tabeli rashod_opreme, a nalog nije proknjizen - ako se ovo ne uradi
                        moze u vise naloga da se nadje isto osnovno sredstvo '''
            postoji_u_rashodu_opreme = self.model.os_postoji_u_tabeli_rashod(pronadjen[0][0])
            if not postoji_u_rashodu_opreme:
                if pronadjen[0][10] > datum_rashoda:
                    messagebox.showwarning("Greška", "Ovo osnovno sredstvo je nabavljeno nakon datuma rashoda!", parent=self.view.prozor_nalog_rashoda)
                else:
                    ''' uraditi amortizaciju rashoda za to osnovno sredstvo'''
                    self.uradi_amortizaciju_rashoda(pronadjen)
                    self.view.unos_inventarni_broj.delete(0, 'end')
                    ''' upisati podatke u tabelu rashod opreme'''
            else:
                messagebox.showwarning("Greška", "Ovo osnovno sredstvo se već nalazi u nekom neproknjiženom nalogu rashoda!",
                                       parent=self.view.prozor_nalog_rashoda)
                self.view.unos_inventarni_broj.delete(0, 'end')
        else:
            messagebox.showwarning("Greška", "Ne postoji aktivno osnovno sredstvo sa izabranim inventarnim brojem!",
                                   parent=self.view.prozor_nalog_rashoda)
            self.view.unos_inventarni_broj.delete(0, 'end')

    def kreiraj(self, datum_naloga, broj, danasnji_datum):
        ''' unesi podatke o nalogu u tabelu rashoda '''
        try:
            self.model.kreiraj_rashod(datum_naloga, broj, danasnji_datum)
            ''' otvori prozor za unos osnovnih sredstava za rashod '''
            ''' prvo pronaci id rashoda - poslednji zapis u tabeli rashod '''
            poslednji_nalog = self.model.pronadji_poslednji()
            self.view.rashod_id.set(poslednji_nalog[0][0])
            self.view.otvori_prozor_uradi_rashod(poslednji_nalog)

        except ValueError:
            messagebox.showwarning("Hmmmmmm", "Nešto nije u redu!",
                                   parent=self.view.rashod_frame)

    def datum_rashoda(self):
        return self.view.datum_rashoda.get_date()

    def kreiraj_nalog_rashod(self):
        datum_rashoda = self.datum_rashoda()
        datum_naloga = datum_rashoda.strftime('%Y-%m-%d')
        broj_naloga = self.view.broj_dokumenta.get()
        amort_model = AmortizacijaModel()
        amortizacija_posle = amort_model.amortizacija_posle_datuma(datum_naloga)
        if not broj_naloga:
            messagebox.showwarning("Greška", "Morate uneti broj dokumenta!",
                                   parent=self.view.rashod_frame)
        elif amortizacija_posle:
            messagebox.showwarning("Greška", "Postoji uradjena amortizacija na dan ili posle datuma rashoda, ne možete da radite rashod na ovaj datum!",
                                   parent=self.view.rashod_frame)
        else:
            danasnji_datum = date.today()
            datum_kreiranja_sistemski = danasnji_datum.strftime('%Y-%m-%d')
            self.kreiraj(datum_naloga, broj_naloga, datum_kreiranja_sistemski)
            self.view.my_tree_rashod.delete(*self.view.my_tree_rashod.get_children())

    def stampanje_rashoda(self):
        id_rashoda = self.view.rashod_id.get()
        podaci_za_stampu = self.podaci_za_izvestaj(id_rashoda)
        podaci_za_stampu_grupisani = self.podaci_za_izvestaj_grupisani(id_rashoda)
        # print(podaci_za_stampu_grupisani)
        ''' podaci o uradjenoj amortizacijji '''
        podaci_o_rashodu = self.model.pronadji_nalog_rashoda(id_rashoda)
        # print(podaci_o_rashodu)
        ''' slanje podataka na stampu '''
        try:
            stampa = StampaIzvestaja()
            stampa.stampa_izvestaja_rashod(podaci_za_stampu, podaci_za_stampu_grupisani, podaci_o_rashodu)
        except OSError:
            messagebox.showwarning("Greška", "Morate zatvoriti prethodni PDF izveštaj rashoda!", parent=self.view.rashod_frame)

    def obrisi_red(self):
        izabrani_red = self.izaberi_red_os(e=None)
        if izabrani_red:
            # Pronadji rashod
            pronadjen_os_tabela_rashod_opreme = self.model.os_postoji_u_tabeli_rashod(izabrani_red)
            self.model.obrisi_os_rashod_opreme(pronadjen_os_tabela_rashod_opreme[0][2])

            nalog_id = self.view.id_naloga
            self.nalog_list_os_za_rashod(nalog_id)
        else:
            messagebox.showwarning("Greška", "Hmmmmm, niste izabrali ni jedno osnovno sredstvo za brisanje!",
                                   parent=self.view.prozor_nalog_rashoda)

    def izaberi_red_os(self, e):
        return self.view.my_tree_rashod_tabela.focus()

    def poruka_brisanje(self):
        ''' prvo ide provera da li je nalog proknjizen, ako jeste ide poruka da se nalog ne moze izbrisati '''
        izabrani_nalog = self.izaberi_red_rashoda(e=None)
        if izabrani_nalog:
            pronadjen_nalog = self.model.pronadji_nalog_rashoda(izabrani_nalog)
            if pronadjen_nalog[0][3] == 1:
                messagebox.showwarning("Greška", "Ne možete da obrišete proknjižen nalog!!!",
                                       parent=self.view.prozor_spisak_rashoda)
            else:
                self.view.prozor_za_brisanje(pronadjen_nalog[0][0])
        else:
            messagebox.showwarning("Greška", "Hmmmmm, niste izabrali ni jedan nalog!",
                                   parent=self.view.prozor_spisak_rashoda)
        '''otvaranje prozora Da li ste sigurni da hocete da obrisete nalog rashoda'''

    def obrisi_rashod(self, nalog_id):
        '''obrisi nalog iz tabele, i proveri da li ima opreme u njemu, pa obrisi i opremu iz naloga rashod_opreme'''
        rashodovana_oprema = self.model.proveri_oprema_u_nalogu_rashoda(nalog_id)
        if rashodovana_oprema:
            self.model.obrisi_stavke_rashod_opreme(nalog_id)
            self.model.obrisi_nalog_rashoda(nalog_id)
        else:
            self.model.obrisi_nalog_rashoda(nalog_id)
        ''' skloniti dijalog box - Da li zelite da obrisete rashod '''
        self.view.prozor_brisanje.destroy()
        self.list_svi_rashodi()

    def izaberi_red_rashoda(self, e):
        return self.view.my_tree_svi_rashodi.focus()

    def proknjizi_rashod(self):
        nalog_id = self.view.id_naloga

        ''' azurirati tabelu osnovnih sredstava tako da osnovno sredstvo ima status rashodovano'''
        oprema_za_rashod = self.pronadji_os_u_nalogu(nalog_id)
        if not oprema_za_rashod:
            messagebox.showwarning("Hmmmmmmm", "Nemate ni jedno osnovno sredstvo za rashod, ne mozete proknjižiti prazan nalog!!!",
                                   parent=self.view.prozor_nalog_rashoda)
        else:
            os_model = OsnovnoSredstvoModel()
            for oprema in oprema_za_rashod:
                os_model.rashoduj_osnovno_sredstvo(oprema[0])

            ''' azurirati rashod tako da polje proknjizen bude 1 '''
            self.model.azuriraj_tabela_rashod_proknjizen(nalog_id)
            ''' ponovo ucitaj listu spiska naloga rashoda da bi se azuriralo polje proknjizen '''
            self.list_svi_rashodi()
            #self.view.otvori_prozor_spisak_rashoda()
            ''' zatvori prozor '''
            self.view.prozor_nalog_rashoda.destroy()

    def pregledaj_rashod(self, e=None):
        # Pronalazenje ID rashoda na osnovu klika
        selected = self.view.my_tree_svi_rashodi.focus()
        if selected:
            # Pronadji rashod
            pronadjen_rashod = self.model.pronadji_nalog_rashoda(selected)
            self.view.rashod_id.set(selected)
            self.view.otvori_prozor_uradi_rashod(pronadjen_rashod)

        else:
            messagebox.showwarning("Greška", "Hmmmmm, niste izabrali ni jedan nalog!",
                                   parent=self.view.prozor_spisak_rashoda)

    def spisak_rashoda(self):
        ''' pronadji sve uradjene rashode sortirane po id '''
        return self.model.pronadji_sve_uradjene_rashode()

    def list_svi_rashodi(self):
        # Brisanje tabele zbog azuriranja
        self.view.my_tree_svi_rashodi.delete(*self.view.my_tree_svi_rashodi.get_children())
        # povezivanje na bazu i preuzimanje dobavljaca iz tabele
        rezultat = self.spisak_rashoda()
        self.view.my_tree_svi_rashodi.tag_configure('oddrow', background="white")
        self.view.my_tree_svi_rashodi.tag_configure('evenrow', background="lightblue")
        self.view.my_tree_svi_rashodi.tag_configure('neproknjizen', background="#ffcbcb")

        count_rashod = 0
        for record in rezultat:
            if record[3] == 0:
                proknjizen = "Ne"
            else:
                proknjizen = "Da"

            if count_rashod % 2 == 0:
                if proknjizen == "Da":
                    self.view.my_tree_svi_rashodi.insert(parent='', index='end', iid=record[0], text='',
                                                          values=(
                                                          record[2].capitalize(), record[1].strftime("%d.%m.%Y"), proknjizen),
                                                          tags=('evenrow',))
                else:
                    self.view.my_tree_svi_rashodi.insert(parent='', index='end', iid=record[0], text='',
                                                         values=(
                                                             record[2].capitalize(), record[1].strftime("%d.%m.%Y"),
                                                             proknjizen),
                                                         tags=('neproknjizen',))
            else:
                if proknjizen == "Da":
                    self.view.my_tree_svi_rashodi.insert(parent='', index='end', iid=record[0], text='',
                                                          values=(
                                                          record[2].capitalize(), record[1].strftime("%d.%m.%Y"), proknjizen),
                                                          tags=('oddrow',))
                else:
                    self.view.my_tree_svi_rashodi.insert(parent='', index='end', iid=record[0], text='',
                                                         values=(
                                                             record[2].capitalize(), record[1].strftime("%d.%m.%Y"),
                                                             proknjizen),
                                                         tags=('neproknjizen',))
            count_rashod += 1

    def podaci_za_izvestaj(self, nalog_id):
        return self.model.podaci_rashod_opreme(nalog_id)

    def podaci_za_izvestaj_grupisani(self, nalog_id):
        return self.model.podaci_rashod_opreme_grupisani(nalog_id)

    def izabrani_rashod(self):
        selected = self.izaberi_red_rashoda(e=None)
        if selected:
            # Pronadji rashod_opreme
            pronadjen_rashod_opreme = self.podaci_za_izvestaj(selected)
            #print(pronadjen_rashod_opreme)
            self.view.rashod_id.set(selected)
            '''popuniti tabelu na glavnoj strani rashoda'''
            podaci_o_rashodu = self.model.pronadji_nalog_rashoda(selected)
            self.view.naziv_rashoda.config(text=podaci_o_rashodu[0][2].capitalize() + " od " + podaci_o_rashodu[0][1].strftime("%d.%m.%Y."))

            self.lista_spisak_opreme_rashod_podaci(pronadjen_rashod_opreme)
            '''zatvori prozor izbor svih rashoda'''
            self.view.prozor_spisak_rashoda.destroy()
        else:
            messagebox.showwarning("Greška", "Hmmmmm, niste izabrali ni jedan nalog!", parent=self.view.prozor_spisak_rashoda)

    ''' Popuni tabelu sa spiskom opreme koja se rashoduje sa iznosima '''
    def lista_spisak_opreme_rashod_podaci(self, lista):
        # Brisanje tabele zbog azuriranja
        self.view.my_tree_rashod.delete(*self.view.my_tree_rashod.get_children())
        ''' Ovde ide upit za dobijanje spiska opreme iz tabele rashod opreme koja ima id_naloga'''

        count_oprema = 0
        for record in lista:
            nabavna_vrednost = locale.format_string('%10.2f', record[2], grouping=True)
            amortizovana_vrednost = locale.format_string('%10.2f', record[3], grouping=True)
            otpisana_vrednost = locale.format_string('%10.2f', record[4], grouping=True)
            preostala = record[2]-(record[3]+record[4])
            preostala_vrednost = locale.format_string('%10.2f', preostala, grouping=True)
            if count_oprema % 2 == 0:
                self.view.my_tree_rashod.insert(parent='', index='end', iid=count_oprema, text='',
                                                     values=(
                                                         count_oprema+1, record[0], record[1], nabavna_vrednost, amortizovana_vrednost, otpisana_vrednost, preostala_vrednost),
                                                     tags=('evenrow',))
            else:
                self.view.my_tree_rashod.insert(parent='', index='end', iid=count_oprema, text='',
                                                     values=(
                                                         count_oprema+1, record[0], record[1], nabavna_vrednost, amortizovana_vrednost, otpisana_vrednost, preostala_vrednost),
                                                     tags=('oddrow',))
            count_oprema += 1
