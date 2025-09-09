from tkinter import ttk, Label, Frame, Button, LabelFrame, Entry, Canvas, Toplevel, IntVar
from controllers.dimenzije_prozora import DimenzijeProzora
from tkcalendar import DateEntry
import tkinter as tk


class UnosView:
    def __init__(self, master):
        self.master = master
        self.prozor_brisanje = None
        self.prozor_nabavka = None
        self.prvi_frame_naslov = None
        self.dobavljac_label_naslov = None
        self.dobavljac_naslov = None
        self.faktura = None
        self.broj_fakture_label = None
        self.broj_dokumenta_label = None
        self.broj_dokumenta = None
        self.datum_dokumenta_label = None
        self.datum_dokumenta = None
        self.proknjizen_label = None
        self.proknjizen_da_ne = None
        self.drugi_frame_unos = None
        self.levi_frame = None
        self.srednji_frame = None
        self.desni_frame = None
        self.inventarni_broj_label = None
        self.inventarni_broj_entry = None
        self.generisi = None
        self.naziv_label = None
        self.naziv_entry = None
        self.nabavna_entry = None
        self.nabavna_label = None
        self.otpisana_label = None
        self.otpisana_entry = None
        self.status_label = None
        self.spisak_statusa = None
        self.status_combo = None
        self.status_prikaz = None
        self.konto_label = None
        self.spisak_konta = None
        self.konto_combo = None
        self.konto_prikaz = None
        self.stopa_label = None
        self.stopa_label_iznos = None
        self.stopa_dugme = None
        self.id_izabrane_stope = None
        self.lokacija_label = None
        self.dictionary_lokacije = None
        self.spisak_lokacija = None
        self.izabrana_lokacija = None
        self.zaduzenje_label = None
        self.dictionary_zaposlenih = None
        self.spisak_zaposlenih = None
        self.zaduzenje_combo = None
        self.linija = None
        self.dugme_dodaj = None
        self.dugme_izmeni = None
        self.dugme_obrisi = None
        self.treci_frame_tabela = None
        self.canvas_tabela_nabavka = None
        self.style = None
        self.treeScroll = None
        self.tree_tabela_nabavka = None
        self.id_izmenjene_opreme = None
        self.cetvrti_frame = None
        self.dugme_proknjizi = None
        self.dugme_stampaj = None
        self.prozor_izbor_stope = None
        self.prvi_frame_prozor_stope = None
        self.canvas_stope = None
        self.my_tree_sve_stope = None
        self.treeVrstaScroll = None
        self.drugi_frame_dugme = None
        self.dugme_izaberi_stopu = None
        self.controller = None
        self.unos_frame = None
        self.unos_novog = None
        self.datum_nabavke_label = None
        self.datum_nabavke = None
        self.dobavljac_label = None
        self.lista_dobavljaca = None
        self.unet_naziv_dobavljaca = None
        self.broj_fakture = None
        self.kreiraj_nalog = None
        self.pregled_nabavki = None
        self.naslov_tabele = None
        self.canvas_pregled = None
        self.my_tree_pregled_nabavki = None
        self.treePregledScroll = None
        self.komande = None
        self.dugme_otvori = None

    def prozor_za_brisanje(self, id_fakture):
        self.prozor_brisanje = Toplevel(self.master)
        self.prozor_brisanje.rowconfigure(0, weight=1)
        self.prozor_brisanje.rowconfigure(1, weight=1)
        self.prozor_brisanje.columnconfigure(0, weight=1)
        self.prozor_brisanje.columnconfigure(1, weight=1)
        window_height = 120
        window_width = 250
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.prozor_brisanje.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_brisanje.title("Brisanje rashoda")
        self.prozor_brisanje.resizable(None, None)
        self.prozor_brisanje.grab_set()

        pitanje_label = Label(self.prozor_brisanje, text="Da li ste sigurni?")
        pitanje_label.grid(row=0, column=0, pady=20, sticky='nsew', columnspan=2)
        dugme_da = Button(self.prozor_brisanje, text='Da', bg='lightblue',
                          command=lambda: self.controller.obrisi_ulaznu_fakturu(id_fakture))
        dugme_da.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        dugme_odustani = Button(self.prozor_brisanje, text='Ne', bg='white', command=self.prozor_brisanje.destroy)
        dugme_odustani.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    def otvori_prozor_nabavke(self, id_naloga):
        self.prozor_nabavka = Toplevel(self.master)
        self.prozor_nabavka.grab_set()
        self.prozor_nabavka.title("Dokument nabavke osnovnog sredstva")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        dimenzije = DimenzijeProzora(screen_width, screen_height)
        window_width = dimenzije.odredi_sirinu_kreiran_nalog()
        window_height = dimenzije.odredi_visinu_kreiran_nalog()

        screen_width = self.master.winfo_screenwidth()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = 0
        self.prozor_nabavka.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_nabavka.columnconfigure(0, weight=1)
        self.prozor_nabavka.rowconfigure(0, weight=1)
        self.prozor_nabavka.rowconfigure(1, weight=1)
        self.prozor_nabavka.rowconfigure(2, weight=3)
        self.prozor_nabavka.rowconfigure(3, weight=1)
        self.prozor_nabavka.rowconfigure(4, weight=1)

        self.faktura = id_naloga
        podaci = self.controller.podaci_za_nalog_nabavke(id_naloga)
        broj_fakture = podaci[0][0]
        datum_fakture = podaci[0][1]
        proknjizen = podaci[0][2]
        dobavljac_naziv = podaci[0][3]
        dobavljac_mesto = podaci[0][4]
        #############################################################################################
        # Prvi frame broj i datum naloga
        self.prvi_frame_naslov = Frame(self.prozor_nabavka)
        self.prvi_frame_naslov.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        self.prvi_frame_naslov.columnconfigure(0, weight=1)
        self.prvi_frame_naslov.columnconfigure(1, weight=1)
        self.prvi_frame_naslov.rowconfigure(0, weight=1)
        self.prvi_frame_naslov.rowconfigure(1, weight=1)
        # Label - dobavljac
        self.dobavljac_label_naslov = Label(self.prvi_frame_naslov, text='Dobavljač', font=(None, 10, 'bold'))
        self.dobavljac_label_naslov.grid(row=0, column=0, padx=10, sticky='e')
        self.dobavljac_naslov = Label(self.prvi_frame_naslov, text=dobavljac_naziv + ", " + dobavljac_mesto,
                                      font=(None, 12, 'bold'))
        self.dobavljac_naslov.grid(row=0, column=1, padx=10, sticky='w')
        # Label - broj naloga
        self.broj_dokumenta_label = Label(self.prvi_frame_naslov, text="Broj dokumenta", font=(None, 10, 'bold'))
        self.broj_dokumenta_label.grid(row=1, column=0, padx=10, sticky='e')
        self.broj_dokumenta = Label(self.prvi_frame_naslov, text=broj_fakture, font=(None, 12, 'bold'), justify="center")
        self.broj_dokumenta.grid(row=1, column=1, padx=10, sticky='w')
        # Label - datum naloga
        self.datum_dokumenta_label = Label(self.prvi_frame_naslov, text="Datum dokumenta", font=(None, 10, 'bold'))
        self.datum_dokumenta_label.grid(row=2, column=0, padx=10, sticky='e')
        self.datum_dokumenta = Label(self.prvi_frame_naslov, text=datum_fakture.strftime("%d.%m.%Y."), font=(None, 12, 'bold'))
        self.datum_dokumenta.grid(row=2, column=1, padx=10, sticky='w')
        # Label da li je proknjizen
        self.proknjizen_label = Label(self.prvi_frame_naslov, text="Proknjižen", font=(None, 10, 'bold'))
        self.proknjizen_label.grid(row=3, column=0, padx=10, sticky='e')
        if proknjizen == 0:
            self.proknjizen_da_ne = Label(self.prvi_frame_naslov, text="Ne", font=(None, 12, 'bold'))
        else:
            self.proknjizen_da_ne = Label(self.prvi_frame_naslov, text="Da", font=(None, 12, 'bold'))
        self.proknjizen_da_ne.grid(row=3, column=1, padx=10, sticky='w')

        ########################################################################################################
        # Drugi frame unos podataka o osnovnom sredstvu
        self.drugi_frame_unos = LabelFrame(self.prozor_nabavka, text="Unos podataka o osnovnom sredstvu", bg="lightblue")
        self.drugi_frame_unos.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.drugi_frame_unos.columnconfigure(0, weight=1)
        self.drugi_frame_unos.columnconfigure(1, weight=1)
        self.drugi_frame_unos.columnconfigure(2, weight=1)
        self.drugi_frame_unos.rowconfigure(0, weight=1)

        self.levi_frame = Frame(self.drugi_frame_unos, bg="lightblue")
        self.levi_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.srednji_frame = Frame(self.drugi_frame_unos, bg="lightblue")
        self.srednji_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.desni_frame = Frame(self.drugi_frame_unos, bg="lightblue")
        self.desni_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Levi frame
        self.inventarni_broj_label = Label(self.levi_frame, text='Inventarni broj:', bg="lightblue")
        self.inventarni_broj_label.grid(row=0, column=0, padx=10, sticky='e')

        self.inventarni_broj_entry = Entry(self.levi_frame, justify='center', font=('Helvetica', 10))
        self.inventarni_broj_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.generisi = Button(self.levi_frame, text="Generisi inv.broj", command=self.controller.generisi_inv_broj)
        self.generisi.grid(row=0, column=2, padx=10, sticky='ew')

        self.naziv_label = Label(self.levi_frame, text="Naziv", bg="lightblue")
        self.naziv_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.naziv_entry = Entry(self.levi_frame, font=('Helvetica', 10), justify="center")
        self.naziv_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.naziv_entry.bind("<KeyRelease>", self.controller.proveri_jezik_naziv)

        self.nabavna_label = Label(self.levi_frame, text="Nabavna vrednost", bg="lightblue")
        self.nabavna_label.grid(row=2, column=0, padx=10, sticky="e")
        self.nabavna_entry = Entry(self.levi_frame, justify="right")
        self.nabavna_entry.grid(row=2, column=1, padx=10, sticky='ew')
        self.nabavna_entry.bind("<Return>", self.controller.provera_broj_nabavna)
        self.nabavna_entry.bind("<Leave>", self.controller.provera_broj_nabavna, add="+")

        # Srednji frame
        self.otpisana_label = Label(self.srednji_frame, text="Otpisana vrednost", bg="lightblue")
        self.otpisana_label.grid(row=0, column=0, padx=10, sticky="e")
        self.otpisana_entry = Entry(self.srednji_frame, justify="right")
        self.otpisana_entry.grid(row=0, column=1, padx=10, sticky='ew')
        self.otpisana_entry.bind("<Return>", self.controller.provera_broj_otpisana)
        self.otpisana_entry.bind("<Leave>", self.controller.provera_broj_otpisana, add="+")

        self.status_label = Label(self.srednji_frame, text="Status", bg="lightblue")
        self.status_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.spisak_statusa = ['aktivno', 'rashodovano', 'amortizovano']
        self.status_combo = ttk.Combobox(self.srednji_frame, font="5", values=self.spisak_statusa, state='readonly', justify="center")
        self.status_combo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.status_combo.current(0)

        self.status_prikaz = Label(self.srednji_frame, text="", bg="lightblue")
        self.status_prikaz.grid(row=1, column=2, padx=10, sticky="ew")

        self.konto_label = Label(self.srednji_frame, text="Konto", bg="lightblue")
        self.konto_label.grid(row=2, column=0, padx=10, sticky="e")

        dictionary_konta = self.controller.dictionary_svih_konta()
        self.spisak_konta = self.controller.lista_svih_konta(dictionary_konta)
        self.konto_combo = ttk.Combobox(self.srednji_frame, font="5", values=self.spisak_konta, state='readonly', justify="center")
        self.konto_combo.grid(row=2, column=1, padx=10, sticky="ew")

        self.konto_prikaz = Label(self.srednji_frame, text="", bg="lightblue")
        self.konto_prikaz.grid(row=2, column=2, padx=10, sticky="ew")

        # Desni frame
        self.stopa_label = Label(self.desni_frame, text="Stopa", bg="lightblue")
        self.stopa_label.grid(row=0, column=0, padx=10, sticky='e')

        self.stopa_label_iznos = Label(self.desni_frame, text="", bg="lightblue", borderwidth=2, relief="groove", justify="center")
        self.stopa_label_iznos.grid(row=0, column=1, padx=10, sticky="ew")

        self.stopa_dugme = Button(self.desni_frame, text="Izaberi stopu", command=self.otvori_prozor_stope)
        self.stopa_dugme.grid(row=0, column=2, padx=10, sticky="ew")
        self.id_izabrane_stope = IntVar()

        self.lokacija_label = Label(self.desni_frame, text="Lokacija", bg="lightblue")
        self.lokacija_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.dictionary_lokacije = self.controller.dictionary_svih_lokacija()
        self.spisak_lokacija = self.controller.lista_svih_lokacija(self.dictionary_lokacije)
        self.izabrana_lokacija = ttk.Combobox(self.desni_frame, values=self.spisak_lokacija, state='readonly', justify="center")
        self.izabrana_lokacija.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.izabrana_lokacija.current(0)

        self.zaduzenje_label = Label(self.desni_frame, text="Zaduženje", bg="lightblue")
        self.zaduzenje_label.grid(row=2, column=0, padx=10, sticky="e")
        self.dictionary_zaposlenih = self.controller.dictionary_svih_zaposlenih()
        self.spisak_zaposlenih = self.controller.lista_svih_zaposlenih(self.dictionary_zaposlenih)
        self.zaduzenje_combo = ttk.Combobox(self.desni_frame, values=self.spisak_zaposlenih, state='readonly', justify="center")
        self.zaduzenje_combo.grid(row=2, column=1, padx=10, sticky="ew")
        self.zaduzenje_combo.current(0)

        self.linija = ttk.Separator(self.drugi_frame_unos, orient="horizontal")
        self.linija.grid(row=1, column=0, columnspan=3, padx=10, sticky="ew")

        # Dugmad
        if proknjizen == 1:
            self.dugme_dodaj = Button(self.drugi_frame_unos, text="Dodaj osnovno sredstvo", bg="#72D473", state='disabled', command=self.controller.proknjizi_osnovno_sredstvo)
        else:
            self.dugme_dodaj = Button(self.drugi_frame_unos, text="Dodaj osnovno sredstvo", bg="#72D473", command=self.controller.proknjizi_osnovno_sredstvo)
        self.dugme_dodaj.grid(row=2, column=0, padx=50, pady=10, sticky="ew")

        if proknjizen == 1:
            self.dugme_izmeni = Button(self.drugi_frame_unos, text="Izmeni osnovno sredstvo", state='disabled', command=self.controller.izmeni_red)
        else:
            self.dugme_izmeni = Button(self.drugi_frame_unos, text="Izmeni osnovno sredstvo", command=self.controller.izmeni_red)
        self.dugme_izmeni.grid(row=2, column=1, padx=50, pady=10, sticky="ew")

        if proknjizen == 1:
            self.dugme_obrisi = Button(self.drugi_frame_unos, text="Obriši osnovno sredstvo", bg="#ffcbcb", state='disabled', command=self.controller.obrisi_red)
        else:
            self.dugme_obrisi = Button(self.drugi_frame_unos, text="Obriši osnovno sredstvo", bg="#ffcbcb", command=self.controller.obrisi_red)
        self.dugme_obrisi.grid(row=2, column=2, padx=50, pady=10, sticky="ew")

        ##############################################################################################################
        ''' Treci frame tabela '''
        self.treci_frame_tabela = Frame(self.prozor_nabavka)
        self.treci_frame_tabela.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.treci_frame_tabela.columnconfigure(0, weight=1)
        self.treci_frame_tabela.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_tabela_nabavka = Canvas(self.treci_frame_tabela)
        self.canvas_tabela_nabavka.grid(row=0, column=0, sticky='nsew')
        self.canvas_tabela_nabavka.columnconfigure(0, weight=1)
        self.canvas_tabela_nabavka.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])
        self.tree_tabela_nabavka = ttk.Treeview(self.canvas_tabela_nabavka)
        self.tree_tabela_nabavka.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.tree_tabela_nabavka['columns'] = ("R.br", "Inv.broj", "Naziv", "Nabavna", "Otpisana", "Status", "Konto", "Stopa", "Korisnik", "Lokacija")
        self.tree_tabela_nabavka.column("#0", width=0, stretch=False)
        self.tree_tabela_nabavka.column("R.br", anchor=tk.CENTER, width=5)
        self.tree_tabela_nabavka.column("Inv.broj", anchor=tk.CENTER, width=10)
        self.tree_tabela_nabavka.column("Naziv", anchor=tk.W, minwidth=40)
        self.tree_tabela_nabavka.column("Nabavna", anchor=tk.E, width=20)
        self.tree_tabela_nabavka.column("Otpisana", anchor=tk.E, width=20)
        self.tree_tabela_nabavka.column("Status", anchor=tk.CENTER, width=10)
        self.tree_tabela_nabavka.column("Konto", anchor=tk.CENTER, width=10)
        self.tree_tabela_nabavka.column("Stopa", anchor=tk.CENTER, width=10)
        self.tree_tabela_nabavka.column("Korisnik", anchor=tk.CENTER, minwidth=10)
        self.tree_tabela_nabavka.column("Lokacija", anchor=tk.CENTER, minwidth=10)

        self.treeScroll = ttk.Scrollbar(self.canvas_tabela_nabavka)
        self.treeScroll.grid(row=0, column=1, sticky='ns')
        self.treeScroll.configure(command=self.tree_tabela_nabavka.yview)
        self.tree_tabela_nabavka.configure(yscrollcommand=self.treeScroll.set)

        self.tree_tabela_nabavka.heading("#0", anchor=tk.W, text="")
        self.tree_tabela_nabavka.heading("R.br", anchor=tk.CENTER, text="R.br")
        self.tree_tabela_nabavka.heading("Inv.broj", anchor=tk.CENTER, text="Inv.broj")
        self.tree_tabela_nabavka.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.tree_tabela_nabavka.heading("Nabavna", anchor=tk.CENTER, text="Nabavna")
        self.tree_tabela_nabavka.heading("Otpisana", anchor=tk.CENTER, text="Otpisana")
        self.tree_tabela_nabavka.heading("Status", anchor=tk.CENTER, text="Status")
        self.tree_tabela_nabavka.heading("Konto", anchor=tk.CENTER, text="Konto")
        self.tree_tabela_nabavka.heading("Stopa", anchor=tk.CENTER, text="Stopa")
        self.tree_tabela_nabavka.heading("Korisnik", anchor=tk.CENTER, text="Korisnik")
        self.tree_tabela_nabavka.heading("Lokacija", anchor=tk.CENTER, text="Lokacija")

        self.controller.prikazi_opremu_tabela_nabavke(id_naloga)
        # Selektovanje reda iz tabele klikom na slog
        self.tree_tabela_nabavka.bind("<ButtonRelease-1>", self.controller.izaberi_red_oprema)
        self.id_izmenjene_opreme = IntVar()
        # Cetvrti frame dugmad Proknjizi i Stampaj
        self.cetvrti_frame = Frame(self.prozor_nabavka, bg="lightblue")
        self.cetvrti_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.cetvrti_frame.columnconfigure(0, weight=1)
        self.cetvrti_frame.columnconfigure(1, weight=1)
        self.cetvrti_frame.columnconfigure(2, weight=1)
        self.cetvrti_frame.columnconfigure(3, weight=1)
        self.cetvrti_frame.columnconfigure(4, weight=1)
        self.cetvrti_frame.columnconfigure(5, weight=1)
        self.cetvrti_frame.rowconfigure(0, weight=1)

        if proknjizen == 1:
            self.dugme_proknjizi = Button(self.cetvrti_frame, text="Proknjiži", bg="#5887C2", fg="white", state='disabled', command=self.controller.proknjizi_fakturu)
        else:
            self.dugme_proknjizi = Button(self.cetvrti_frame, text="Proknjiži", bg="#5887C2", fg="white", command=self.controller.proknjizi_fakturu)
        self.dugme_proknjizi.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        if proknjizen == 0:
            self.dugme_stampaj = Button(self.cetvrti_frame, state='disabled', text="Štampaj", command=self.controller.stampa_fakture)
        else:
            self.dugme_stampaj = Button(self.cetvrti_frame, text="Štampaj", command=self.controller.stampa_fakture)
        self.dugme_stampaj.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    def otvori_prozor_stope(self):
        self.prozor_izbor_stope = Toplevel(self.prozor_nabavka)
        self.prozor_izbor_stope.grab_set()
        self.prozor_izbor_stope.title("Izbor amortizacione stope")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 800
        window_height = 400
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.prozor_izbor_stope.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_izbor_stope.resizable(False, False)
        self.prozor_izbor_stope.columnconfigure(0, weight=1)
        self.prozor_izbor_stope.rowconfigure(0, weight=1)
        self.prozor_izbor_stope.rowconfigure(1, weight=1)

        ''' ********** Prvi frame tabela sa amortizacionim stopama ************ '''
        self.prvi_frame_prozor_stope = Frame(self.prozor_izbor_stope)
        self.prvi_frame_prozor_stope.grid(row=0, column=0, padx=10, sticky='ew')
        self.prvi_frame_prozor_stope.columnconfigure(0, weight=1)
        self.prvi_frame_prozor_stope.rowconfigure(0, weight=1)
        self.prvi_frame_prozor_stope.rowconfigure(1, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_stope = Canvas(self.prvi_frame_prozor_stope)
        self.canvas_stope.grid(row=0, column=0, sticky='nsew')
        self.canvas_stope.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_sve_stope = ttk.Treeview(self.canvas_stope)
        self.my_tree_sve_stope.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_sve_stope['columns'] = ("Oznaka", "Naziv", "Stopa")
        self.my_tree_sve_stope.column("#0", width=0, stretch=False)
        self.my_tree_sve_stope.column("Oznaka", anchor=tk.CENTER, width=30)
        self.my_tree_sve_stope.column("Naziv", anchor=tk.W, minwidth=250)
        self.my_tree_sve_stope.column("Stopa", anchor=tk.CENTER, width=30)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeVrstaScroll = ttk.Scrollbar(self.canvas_stope)
        self.treeVrstaScroll.grid(row=0, column=1, sticky='ns')
        self.treeVrstaScroll.configure(command=self.my_tree_sve_stope.yview)
        self.my_tree_sve_stope.configure(yscrollcommand=self.treeVrstaScroll.set)

        self.my_tree_sve_stope.heading("#0", anchor=tk.W, text="")
        self.my_tree_sve_stope.heading("Oznaka", anchor=tk.CENTER, text="Oznaka")
        self.my_tree_sve_stope.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_sve_stope.heading("Stopa", anchor=tk.CENTER, text="Stopa")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_sve_stope.tag_configure('oddrow', background="white")
        self.my_tree_sve_stope.tag_configure('evenrow', background="lightblue")

        # Prikaz svih vrsta naloga u tabeli
        self.controller.list_sve_stope()

        ''' ********** Drugi frame dugme izaberi stopu ************** '''
        self.drugi_frame_dugme = Frame(self.prozor_izbor_stope)
        self.drugi_frame_dugme.grid(row=1, column=0, padx=10, sticky='ew')
        self.drugi_frame_dugme.columnconfigure(0, weight=1)
        self.drugi_frame_dugme.rowconfigure(0, weight=1)

        self.dugme_izaberi_stopu = Button(self.drugi_frame_dugme, text="Izaberi amortizacionu stopu", bg="lightblue", command=self.controller.izaberi_stopu)
        self.dugme_izaberi_stopu.grid(row=0, column=0, padx=10, pady=10)

    def pokreni(self, controller):
        self.controller = controller
        self.unos_frame = LabelFrame(self.master, text="Unos opreme", font=('Helvetica', 12, 'bold'))
        self.unos_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.unos_frame.columnconfigure(0, weight=1)
        self.unos_frame.rowconfigure(0, weight=1)
        self.unos_frame.rowconfigure(1, weight=6)
        self.unos_frame.rowconfigure(2, weight=1)

        self.unos_novog = LabelFrame(self.unos_frame, text="Nabavka opreme", font=('Helvetica', 9, 'bold'))
        self.unos_novog.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.datum_nabavke_label = Label(self.unos_novog, text="Datum nabavke")
        self.datum_nabavke_label.grid(row=0, column=0, padx=10, pady=5)
        self.datum_nabavke = DateEntry(self.unos_novog, selectmode='day', locale='sr_RS', date_pattern='dd.MM.yyyy', font='5', justify="center")
        self.datum_nabavke.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.dobavljac_label = Label(self.unos_novog, text="Dobavljač")
        self.dobavljac_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        dictionary_dobavljaca = controller.dictionary_svih_dobavljaca()
        self.lista_dobavljaca = controller.lista_svih_dobavljaca(dictionary_dobavljaca)
        self.unet_naziv_dobavljaca = ttk.Combobox(self.unos_novog, font="5", values=self.lista_dobavljaca,
                                                  state="readonly",
                                                  justify="center")
        self.unet_naziv_dobavljaca.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.broj_fakture_label = Label(self.unos_novog, text="Broj dokumenta")
        self.broj_fakture_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.broj_fakture = Entry(self.unos_novog, justify="center")
        self.broj_fakture.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.broj_fakture.bind("<KeyRelease>", self.controller.proveri_jezik_broj_fakture)
        self.kreiraj_nalog = Button(self.unos_novog, text="Kreiraj nalog", bg="lightblue", command=controller.kreiraj_nalog_nabavke)
        self.kreiraj_nalog.grid(row=0, column=2, padx=10, pady=5, rowspan=2, sticky="nsew")

        ''' Tabela sa pregledom ulaznih faktura '''
        self.pregled_nabavki = LabelFrame(self.unos_frame, text="Pregled nabavki", font=('Helvetica', 9, 'bold'))
        self.pregled_nabavki.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.pregled_nabavki.columnconfigure(0, weight=1)
        self.pregled_nabavki.rowconfigure(0, weight=1)
        self.pregled_nabavki.rowconfigure(1, weight=2)
        self.pregled_nabavki.rowconfigure(2, weight=1)

        self.naslov_tabele = Label(self.pregled_nabavki, text="Spisak ulaznih faktura", font=('Helvetica', 14))
        self.naslov_tabele.grid(row=0, column=0, padx=10, pady=0)
        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_pregled = Canvas(self.pregled_nabavki)
        self.canvas_pregled.grid(row=1, column=0, sticky='nsew')
        self.canvas_pregled.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_pregled_nabavki = ttk.Treeview(self.canvas_pregled)
        self.my_tree_pregled_nabavki.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_pregled_nabavki['columns'] = (
            "R.br", "Naziv dobavljača", "Broj dokumenta", "Datum dokumenta", "Proknjižen")
        self.my_tree_pregled_nabavki.column("#0", width=0, stretch=False)
        self.my_tree_pregled_nabavki.column("R.br", anchor=tk.CENTER, width=6)
        self.my_tree_pregled_nabavki.column("Naziv dobavljača", anchor=tk.W, minwidth=50)
        self.my_tree_pregled_nabavki.column("Broj dokumenta", anchor=tk.W, width=40)
        self.my_tree_pregled_nabavki.column("Datum dokumenta", anchor=tk.CENTER, width=10)
        self.my_tree_pregled_nabavki.column("Proknjižen", anchor=tk.CENTER, width=10)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treePregledScroll = ttk.Scrollbar(self.canvas_pregled)
        self.treePregledScroll.grid(row=0, column=1, sticky='ns')
        self.treePregledScroll.configure(command=self.my_tree_pregled_nabavki.yview)
        self.my_tree_pregled_nabavki.configure(yscrollcommand=self.treePregledScroll.set)

        self.my_tree_pregled_nabavki.heading("#0", anchor=tk.W, text="")
        self.my_tree_pregled_nabavki.heading("R.br", anchor=tk.CENTER, text="R.br")
        self.my_tree_pregled_nabavki.heading("Naziv dobavljača", anchor=tk.CENTER, text="Naziv dobavljača")
        self.my_tree_pregled_nabavki.heading("Broj dokumenta", anchor=tk.CENTER, text="Broj dokumenta")
        self.my_tree_pregled_nabavki.heading("Datum dokumenta", anchor=tk.CENTER, text="Datum dokumenta")
        self.my_tree_pregled_nabavki.heading("Proknjižen", anchor=tk.CENTER, text="Proknjižen")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_pregled_nabavki.tag_configure('oddrow', background="white")
        self.my_tree_pregled_nabavki.tag_configure('evenrow', background="lightblue")
        # ovde treba spisak za prikaz u tabeli
        self.controller.sve_nabavke()

        self.komande = Frame(self.unos_frame)
        self.komande.columnconfigure(0, weight=1)
        self.komande.columnconfigure(1, weight=1)
        self.komande.columnconfigure(2, weight=1)
        self.komande.columnconfigure(3, weight=1)
        self.komande.columnconfigure(4, weight=1)
        self.komande.columnconfigure(5, weight=1)

        self.komande.grid(row=2, column=0, padx=10, sticky="ew")
        self.dugme_otvori = Button(self.komande, text="Pregledaj fakturu", bg="lightblue", command=self.controller.pregledaj_nalog_nabavke)
        self.dugme_otvori.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.dugme_obrisi = Button(self.komande, text="Obriši fakturu", bg="#ffcbcb", command=self.controller.obrisi_fakturu)
        self.dugme_obrisi.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
