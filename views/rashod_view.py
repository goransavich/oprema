from tkinter import Button, LabelFrame, Frame, Canvas, Toplevel, Label, IntVar, Entry, ttk
from tkcalendar import DateEntry
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class RashodView:
    def __init__(self, master):
        self.master = master
        self.prozor_brisanje = None
        self.prozor_spisak_rashoda = None
        self.list_svi_rashodi = None
        self.canvas_spisak_rashoda = None
        self.style = None
        self.my_tree_svi_rashodi = None
        self.treeSpisakScroll = None
        self.polje_dugmad_spisak_rashoda = None
        self.dugme_pregledaj_rashod = None
        self.dugme_izaberi_rashod_iz_spiska = None
        self.dugme_obrisi_rashod_iz_spiska = None
        self.prozor_nalog_rashoda = None
        self.id_naloga = None
        self.prvi_frame_naslov = None
        self.broj_naloga_label = None
        self.datum_naloga_label = None
        self.proknjizen_nalog_label = None
        self.proknjizen_nalog = None
        self.linija = None
        self.drugi_frame_dodaj = None
        self.unos_inventarni_broj = None
        self.dugme_dodaj = None
        self.treci_frame_tabela = None
        self.canvas_rashod_tabela = None
        self.my_tree_rashod_tabela = None
        self.treeRashodTabelaScroll = None
        self.polje_dugmad_rashod_opreme = None
        self.dugme_proknjizi_rashod = None
        self.dugme_obrisi_osnovnosr_iz_spiska = None
        self.controller = None
        self.rashod_frame = None
        self.datum_rashoda_label = None
        self.dugme_uradi = None
        self.datum_rashoda = None
        self.broj_dokumenta_label = None
        self.broj_dokumenta = None
        self.dugme_izaberi_rashod = None
        self.naziv_rashoda = None
        self.tabela_frame = None
        self.naslov_rashoda = None
        self.canvas_rashod = None
        self.my_tree_rashod = None
        self.treeRashodScroll = None
        self.rashod_id = None
        self.dugme_stampaj = None

    def prozor_za_brisanje(self, id_naloga):
        self.prozor_brisanje = Toplevel(self.prozor_spisak_rashoda)
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
                          command=lambda: self.controller.obrisi_rashod(id_naloga))
        dugme_da.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        dugme_odustani = Button(self.prozor_brisanje, text='Ne', bg='white', command=self.prozor_brisanje.destroy)
        dugme_odustani.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    def otvori_prozor_spisak_rashoda(self):
        self.prozor_spisak_rashoda = Toplevel(self.master)
        self.prozor_spisak_rashoda.grab_set()
        self.prozor_spisak_rashoda.title("Pregled uradjenih rashoda")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        dimenzije = DimenzijeProzora(screen_width, screen_height)
        window_width = dimenzije.odredi_sirinu_prozori_podesavanja()
        window_height = dimenzije.odredi_visinu_prozori_podesavanja()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        if self.master.winfo_screenheight() < 800:
            y_cordinate = 0
        else:
            y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.prozor_spisak_rashoda.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_spisak_rashoda.resizable(False, False)
        self.prozor_spisak_rashoda.columnconfigure(0, weight=1)
        self.prozor_spisak_rashoda.rowconfigure(0, weight=1)
        self.prozor_spisak_rashoda.rowconfigure(1, weight=4)
        self.prozor_spisak_rashoda.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih vrsta naloga - tabela
        self.list_svi_rashodi = Frame(self.prozor_spisak_rashoda)
        self.list_svi_rashodi.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_svi_rashodi.columnconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_spisak_rashoda = Canvas(self.list_svi_rashodi)
        self.canvas_spisak_rashoda.grid(row=0, column=0, sticky='nsew')
        self.canvas_spisak_rashoda.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_svi_rashodi = ttk.Treeview(self.canvas_spisak_rashoda)
        self.my_tree_svi_rashodi.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_svi_rashodi['columns'] = ("Naziv", "Datum", "Proknjižen")
        self.my_tree_svi_rashodi.column("#0", width=0, stretch=False)
        self.my_tree_svi_rashodi.column("Naziv", anchor=tk.CENTER, minwidth=300)
        self.my_tree_svi_rashodi.column("Datum", anchor=tk.CENTER, width=100)
        self.my_tree_svi_rashodi.column("Proknjižen", anchor=tk.CENTER, width=30)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeSpisakScroll = ttk.Scrollbar(self.canvas_spisak_rashoda)
        self.treeSpisakScroll.grid(row=0, column=1, sticky='ns')
        self.treeSpisakScroll.configure(command=self.my_tree_svi_rashodi.yview)
        self.my_tree_svi_rashodi.configure(yscrollcommand=self.treeSpisakScroll.set)

        self.my_tree_svi_rashodi.heading("#0", anchor=tk.W, text="")
        self.my_tree_svi_rashodi.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_svi_rashodi.heading("Datum", anchor=tk.CENTER, text="Datum")
        self.my_tree_svi_rashodi.heading("Proknjižen", anchor=tk.CENTER, text="Proknjižen")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_svi_rashodi.tag_configure('oddrow', background="white")
        self.my_tree_svi_rashodi.tag_configure('evenrow', background="lightblue")

        # Prikaz svih vrsta naloga u tabeli
        self.controller.list_svi_rashodi()

        # Drugi frame za dugmad Izaberi i Obrisi
        self.polje_dugmad_spisak_rashoda = LabelFrame(self.prozor_spisak_rashoda, text="Komande", bg="lightblue")
        self.polje_dugmad_spisak_rashoda.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_spisak_rashoda.rowconfigure(0, weight=1)
        self.polje_dugmad_spisak_rashoda.columnconfigure(0, weight=1)
        self.polje_dugmad_spisak_rashoda.columnconfigure(1, weight=1)
        self.polje_dugmad_spisak_rashoda.columnconfigure(2, weight=1)

        self.dugme_pregledaj_rashod = Button(self.polje_dugmad_spisak_rashoda, text="Udji u nalog", bg="#72D473", command=self.controller.pregledaj_rashod)
        self.dugme_pregledaj_rashod.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.dugme_izaberi_rashod_iz_spiska = Button(self.polje_dugmad_spisak_rashoda, text="Pregledaj rashod", bg="#5887C2", fg="white", command=self.controller.izabrani_rashod)
        self.dugme_izaberi_rashod_iz_spiska.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.dugme_obrisi_rashod_iz_spiska = Button(self.polje_dugmad_spisak_rashoda, text="Obriši rashod", bg="#ffcbcb", command=self.controller.poruka_brisanje)
        self.dugme_obrisi_rashod_iz_spiska.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_svi_rashodi.bind("<ButtonRelease-1>", self.controller.izaberi_red_rashoda)

    def otvori_prozor_uradi_rashod(self, nalog_rashoda):
        self.prozor_nalog_rashoda = Toplevel(self.master)
        self.prozor_nalog_rashoda.grab_set()
        self.prozor_nalog_rashoda.title("Rashod opreme")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        dimenzije = DimenzijeProzora(screen_width, screen_height)
        window_width = dimenzije.odredi_sirinu_prozori_podesavanja()
        window_height = dimenzije.odredi_visinu_prozori_podesavanja()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        if self.master.winfo_screenheight() < 800:
            y_cordinate = 0
        else:
            y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.prozor_nalog_rashoda.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_nalog_rashoda.resizable(False, False)
        self.prozor_nalog_rashoda.columnconfigure(0, weight=1)
        self.prozor_nalog_rashoda.rowconfigure(0, weight=1)
        self.prozor_nalog_rashoda.rowconfigure(1, weight=1)
        self.prozor_nalog_rashoda.rowconfigure(2, weight=3)
        self.prozor_nalog_rashoda.rowconfigure(3, weight=1)

        self.id_naloga = nalog_rashoda[0][0]
        datum_naloga = nalog_rashoda[0][1].strftime('%d.%m.%Y.')
        broj_kreiranog_naloga = nalog_rashoda[0][2]
        proknjizen = nalog_rashoda[0][3]
        if proknjizen == 0:
            da_ne_proknjizen = 'ne'
        else:
            da_ne_proknjizen = 'da'

        #############################################################################################
        # Prvi frame broj i datum naloga
        self.prvi_frame_naslov = Frame(self.prozor_nalog_rashoda)
        self.prvi_frame_naslov.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        self.prvi_frame_naslov.columnconfigure(0, weight=1)
        self.prvi_frame_naslov.columnconfigure(1, weight=1)
        self.prvi_frame_naslov.rowconfigure(0, weight=1)
        self.prvi_frame_naslov.rowconfigure(1, weight=1)
        # Label - broj naloga
        self.broj_naloga_label = Label(self.prvi_frame_naslov, text=broj_kreiranog_naloga, font=(None, 12, 'bold'))
        self.broj_naloga_label.grid(row=0, column=0, padx=10, sticky='e')
        # Label - datum naloga
        self.datum_naloga_label = Label(self.prvi_frame_naslov, text=datum_naloga, font=(None, 12, 'bold'))
        self.datum_naloga_label.grid(row=0, column=1, padx=10, sticky='w')
        # Label - Da li je proknjizen nalog
        self.proknjizen_nalog_label = Label(self.prvi_frame_naslov, text='Proknjižen', font=(None, 10, 'bold'))
        self.proknjizen_nalog_label.grid(row=1, column=0, padx=10, sticky='e')
        # Label - DA/NE
        da_li_je_proknjizen = da_ne_proknjizen.capitalize()
        self.proknjizen_nalog = Label(self.prvi_frame_naslov, text=da_li_je_proknjizen, font=(None, 12, 'bold'))
        self.proknjizen_nalog.grid(row=1, column=1, padx=10, sticky='w')
        self.linija = ttk.Separator(self.prvi_frame_naslov, orient='horizontal')
        self.linija.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        ############################################################################################################
        ''' Drugi frame Dodaj osnovno sredstvo '''
        self.drugi_frame_dodaj = Frame(self.prozor_nalog_rashoda)
        self.drugi_frame_dodaj.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        if proknjizen == 1:
            self.unos_inventarni_broj = Entry(self.drugi_frame_dodaj, state='disabled')
        else:
            self.unos_inventarni_broj = Entry(self.drugi_frame_dodaj)

        self.unos_inventarni_broj.grid(row=0, column=0, padx=10, pady=10)
        self.unos_inventarni_broj.bind("<Return>", self.controller.pronadji_os)
        if proknjizen == 1:
            self.dugme_dodaj = Button(self.drugi_frame_dodaj, text=' + Dodaj osnovno sredstvo', bg='lightblue', command=self.controller.pronadji_os, state='disabled')
        else:
            self.dugme_dodaj = Button(self.drugi_frame_dodaj, text=' + Dodaj osnovno sredstvo', bg='lightblue', command=self.controller.pronadji_os)
        self.dugme_dodaj.grid(row=0, column=1, padx=10, pady=10)

        ############################################################################################################
        ''' Treci frame Tabela sa listom opreme za rashod'''
        self.treci_frame_tabela = Frame(self.prozor_nalog_rashoda)
        self.treci_frame_tabela.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.treci_frame_tabela.columnconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_rashod_tabela = Canvas(self.treci_frame_tabela)
        self.canvas_rashod_tabela.grid(row=0, column=0, sticky='nsew')
        self.canvas_rashod_tabela.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_rashod_tabela = ttk.Treeview(self.canvas_rashod_tabela)
        self.my_tree_rashod_tabela.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_rashod_tabela['columns'] = (
        "R.br", "Inv.broj", "Naziv", "Datum nabavke")
        self.my_tree_rashod_tabela.column("#0", width=0, stretch=False)
        self.my_tree_rashod_tabela.column("R.br", anchor=tk.CENTER, width=10)
        self.my_tree_rashod_tabela.column("Inv.broj", anchor=tk.CENTER, width=20)
        self.my_tree_rashod_tabela.column("Naziv", anchor=tk.W, minwidth=100)
        self.my_tree_rashod_tabela.column("Datum nabavke", anchor=tk.CENTER, width=40)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeRashodTabelaScroll = ttk.Scrollbar(self.canvas_rashod_tabela)
        self.treeRashodTabelaScroll.grid(row=0, column=1, sticky='ns')
        self.treeRashodTabelaScroll.configure(command=self.my_tree_rashod_tabela.yview)
        self.my_tree_rashod_tabela.configure(yscrollcommand=self.treeRashodTabelaScroll.set)

        self.my_tree_rashod_tabela.heading("#0", anchor=tk.W, text="")
        self.my_tree_rashod_tabela.heading("R.br", anchor=tk.CENTER, text="R.br")
        self.my_tree_rashod_tabela.heading("Inv.broj", anchor=tk.CENTER, text="Inv.broj")
        self.my_tree_rashod_tabela.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_rashod_tabela.heading("Datum nabavke", anchor=tk.CENTER, text="Datum nabavke")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_rashod_tabela.tag_configure('oddrow', background="white")
        self.my_tree_rashod_tabela.tag_configure('evenrow', background="lightblue")

        self.controller.nalog_list_os_za_rashod(self.id_naloga)
        #############################################################################################################
        ''' Cetvrti frame Komande'''
        self.polje_dugmad_rashod_opreme = LabelFrame(self.prozor_nalog_rashoda, text="Komande", bg="lightblue")
        self.polje_dugmad_rashod_opreme.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_rashod_opreme.rowconfigure(0, weight=1)
        self.polje_dugmad_rashod_opreme.columnconfigure(0, weight=1)
        self.polje_dugmad_rashod_opreme.columnconfigure(1, weight=1)

        if proknjizen == 1:
            self.dugme_proknjizi_rashod = Button(self.polje_dugmad_rashod_opreme, text="Proknjiži rashod opreme", bg="#5887C2", fg="white", state="disabled", command=self.controller.proknjizi_rashod)
        else:
            self.dugme_proknjizi_rashod = Button(self.polje_dugmad_rashod_opreme, text="Proknjiži rashod opreme", bg="#5887C2", fg="white", command=self.controller.proknjizi_rashod)
        self.dugme_proknjizi_rashod.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        if proknjizen == 1:
            self.dugme_obrisi_osnovnosr_iz_spiska = Button(self.polje_dugmad_rashod_opreme, text=" - Obriši red iz tabele", bg="#ffcbcb", state="disabled", command=self.controller.obrisi_red)
        else:
            self.dugme_obrisi_osnovnosr_iz_spiska = Button(self.polje_dugmad_rashod_opreme, text=" - Obriši red iz tabele", bg="#ffcbcb", command=self.controller.obrisi_red)

        self.dugme_obrisi_osnovnosr_iz_spiska.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_rashod_tabela.bind("<ButtonRelease-1>", self.controller.izaberi_red_os)

    def pokreni(self, controller):
        self.controller = controller
        self.rashod_frame = LabelFrame(self.master, text="Rashod opreme", font=('Helvetica', 12, 'bold'))
        self.rashod_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.rashod_frame.columnconfigure(0, weight=1)
        self.rashod_frame.rowconfigure(0, weight=1)
        self.rashod_frame.rowconfigure(1, weight=2)

        tabovi = ttk.Notebook(self.rashod_frame)
        tabovi.grid(row=0, column=0, sticky='nsew')

        tab1 = Frame(tabovi)
        tab2 = Frame(tabovi)
        tab2.columnconfigure(0, weight=1)
        tab2.rowconfigure(1, weight=1)

        tabovi.add(tab1, text="Uradi rashod")
        tabovi.add(tab2, text="Pregled rashoda")

        ''' prvi tab '''
        self.datum_rashoda_label = Label(tab1, text="Unesi datum rashoda:")
        self.datum_rashoda_label.grid(row=0, column=0, padx=10, pady=10)
        self.datum_rashoda = DateEntry(tab1, selectmode='day', locale='sr_RS', date_pattern='dd.MM.yyyy', font='5')
        self.datum_rashoda.grid(row=0, column=1, padx=10, pady=10)
        self.dugme_uradi = Button(tab1, text="Kreiraj nalog rashoda", command=controller.kreiraj_nalog_rashod, bg="lightblue")
        self.dugme_uradi.grid(row=0, column=2, padx=10, pady=10)
        self.broj_dokumenta_label = Label(tab1, text="Unesi broj dokumenta:")
        self.broj_dokumenta_label.grid(row=1, column=0, padx=10, pady=10)
        self.broj_dokumenta = Entry(tab1)
        self.broj_dokumenta.grid(row=1, column=1, padx=10, pady=10)
        self.broj_dokumenta.bind("<KeyRelease>", self.controller.proveri_jezik_broj_dokumenta)

        ''' drugi tab '''
        self.dugme_izaberi_rashod = Button(tab2, text="Izaberi uradjen rashod", bg="lightblue", command=self.otvori_prozor_spisak_rashoda)
        self.dugme_izaberi_rashod.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.naziv_rashoda = Label(tab2, text="", font=("Helvetica", 12, "bold"))
        self.naziv_rashoda.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="ew")

        ''' tabela '''
        self.tabela_frame = Frame(self.rashod_frame)
        self.tabela_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tabela_frame.columnconfigure(0, weight=1)
        self.tabela_frame.rowconfigure(0, weight=1)
        self.tabela_frame.rowconfigure(1, weight=2)
        self.tabela_frame.rowconfigure(2, weight=1)

        self.naslov_rashoda = Label(self.tabela_frame, text="Pregled rashodovane opreme", font=('Helvetica', 14))
        self.naslov_rashoda.grid(row=0, column=0, padx=10, pady=0)
        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_rashod = Canvas(self.tabela_frame)
        self.canvas_rashod.grid(row=1, column=0, sticky='nsew')
        self.canvas_rashod.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_rashod = ttk.Treeview(self.canvas_rashod)
        self.my_tree_rashod.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_rashod['columns'] = ("R.br", "Inv. broj", "Naziv", "Nabavna vrednost", "Amortizacija rashoda", "Dosadašnji otpis", "Preostala vrednost")
        self.my_tree_rashod.column("#0", width=0, stretch=False)
        self.my_tree_rashod.column("R.br", anchor=tk.CENTER, width=6)
        self.my_tree_rashod.column("Inv. broj", anchor=tk.CENTER, width=10)
        self.my_tree_rashod.column("Naziv", anchor=tk.W, minwidth=50)
        self.my_tree_rashod.column("Nabavna vrednost", anchor=tk.E, width=40)
        self.my_tree_rashod.column("Amortizacija rashoda", anchor=tk.E, width=40)
        self.my_tree_rashod.column("Dosadašnji otpis", anchor=tk.E, width=40)
        self.my_tree_rashod.column("Preostala vrednost", anchor=tk.E, width=40)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeRashodScroll = ttk.Scrollbar(self.canvas_rashod)
        self.treeRashodScroll.grid(row=0, column=1, sticky='ns')
        self.treeRashodScroll.configure(command=self.my_tree_rashod.yview)
        self.my_tree_rashod.configure(yscrollcommand=self.treeRashodScroll.set)

        self.my_tree_rashod.heading("#0", anchor=tk.W, text="")
        self.my_tree_rashod.heading("R.br", anchor=tk.CENTER, text="R.br")
        self.my_tree_rashod.heading("Inv. broj", anchor=tk.CENTER, text="Inv. broj")
        self.my_tree_rashod.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_rashod.heading("Nabavna vrednost", anchor=tk.CENTER, text="Nabavna vrednost")
        self.my_tree_rashod.heading("Amortizacija rashoda", anchor=tk.CENTER, text="Amortizacija rashoda")
        self.my_tree_rashod.heading("Dosadašnji otpis", anchor=tk.CENTER, text="Dosadašnji otpis")
        self.my_tree_rashod.heading("Preostala vrednost", anchor=tk.CENTER, text="Preostala vrednost")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_rashod.tag_configure('oddrow', background="white")
        self.my_tree_rashod.tag_configure('evenrow', background="lightblue")
        self.rashod_id = IntVar()

        self.dugme_stampaj = Button(self.tabela_frame, text="Štampa rashoda", bg="lightblue",
                                    command=controller.stampanje_rashoda)
        self.dugme_stampaj.grid(row=2, column=0, padx=10, pady=10)
