from tkinter import Button, LabelFrame, Frame, ttk, Canvas, Toplevel, Label, IntVar
from tkcalendar import DateEntry
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class Amortizacija:
    def __init__(self, master):
        self.master = master
        self.prozor_brisanje = None
        self.prozor_spisak_amortizacija = None
        self.list_sve_amortizacije = None
        self.canvas_spisak_amortizacija = None
        self.style = None
        self.my_tree_sve_amortizacije = None
        self.treeSpisakScroll = None
        self.polje_dugmad_spisak_amortizacija = None
        self.dugme_obrisi_amortizaciju_iz_spiska = None
        self.dugme_izaberi_amortizaciju_iz_spiska = None
        self.amortizacija_frame = None
        self.controller = None
        self.datum_amortizacije_label = None
        self.datum_amortizacije = None
        self.dugme_uradi = None
        self.dugme_izaberi_amortizaciju = None
        self.naziv_amortizacije = None
        self.tabela_frame = None
        self.naslov_amortizacije = None
        self.canvas_amortizacija = None
        self.my_tree_amortizacija = None
        self.treeAmortizacijaScroll = None
        self.amortizacija_id = None
        self.dugme_stampaj = None
        self.prozor_progres = None
        self.pb = None

    def prozor_za_brisanje(self, id_amortizacije):
        self.prozor_brisanje = Toplevel(self.prozor_spisak_amortizacija)
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
        self.prozor_brisanje.title("Brisanje amortizacije")
        self.prozor_brisanje.resizable(None, None)
        self.prozor_brisanje.grab_set()

        pitanje_label = Label(self.prozor_brisanje, text="Da li ste sigurni?")
        pitanje_label.grid(row=0, column=0, pady=20, sticky='nsew', columnspan=2)
        dugme_da = Button(self.prozor_brisanje, text='Da', bg='lightblue',
                          command=lambda: self.controller.obrisi_amortizaciju(id_amortizacije))
        dugme_da.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        dugme_odustani = Button(self.prozor_brisanje, text='Ne', bg='white', command=self.prozor_brisanje.destroy)
        dugme_odustani.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    def otvori_prozor_spisak_amortizacija(self):
        self.prozor_spisak_amortizacija = Toplevel(self.master)
        self.prozor_spisak_amortizacija.grab_set()
        self.prozor_spisak_amortizacija.title("Pregled uradjenih amortizacija")

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
        self.prozor_spisak_amortizacija.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_spisak_amortizacija.resizable(False, False)
        self.prozor_spisak_amortizacija.columnconfigure(0, weight=1)
        self.prozor_spisak_amortizacija.rowconfigure(0, weight=1)
        self.prozor_spisak_amortizacija.rowconfigure(1, weight=4)
        self.prozor_spisak_amortizacija.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih vrsta naloga - tabela
        self.list_sve_amortizacije = Frame(self.prozor_spisak_amortizacija)
        self.list_sve_amortizacije.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_sve_amortizacije.columnconfigure(0, weight=1)
        # list_sve_vrste_naloga.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_spisak_amortizacija = Canvas(self.list_sve_amortizacije)
        self.canvas_spisak_amortizacija.grid(row=0, column=0, sticky='nsew')
        self.canvas_spisak_amortizacija.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_sve_amortizacije = ttk.Treeview(self.canvas_spisak_amortizacija)
        self.my_tree_sve_amortizacije.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_sve_amortizacije['columns'] = ("Naziv", "Datum")
        self.my_tree_sve_amortizacije.column("#0", width=0, stretch=False)
        self.my_tree_sve_amortizacije.column("Naziv", anchor=tk.CENTER, width=300)
        self.my_tree_sve_amortizacije.column("Datum", anchor=tk.CENTER, minwidth=120)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeSpisakScroll = ttk.Scrollbar(self.canvas_spisak_amortizacija)
        self.treeSpisakScroll.grid(row=0, column=1, sticky='ns')
        self.treeSpisakScroll.configure(command=self.my_tree_sve_amortizacije.yview)
        self.my_tree_sve_amortizacije.configure(yscrollcommand=self.treeSpisakScroll.set)

        self.my_tree_sve_amortizacije.heading("#0", anchor=tk.W, text="")
        self.my_tree_sve_amortizacije.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_sve_amortizacije.heading("Datum", anchor=tk.CENTER, text="Datum")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_sve_amortizacije.tag_configure('oddrow', background="white")
        self.my_tree_sve_amortizacije.tag_configure('evenrow', background="lightblue")

        # Prikaz svih vrsta naloga u tabeli
        self.controller.list_sve_amortizacije()

        # Drugi frame za dugmad Izaberi i Obrisi
        self.polje_dugmad_spisak_amortizacija = LabelFrame(self.prozor_spisak_amortizacija, text="Komande", bg="lightblue")
        self.polje_dugmad_spisak_amortizacija.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_spisak_amortizacija.rowconfigure(0, weight=1)
        self.polje_dugmad_spisak_amortizacija.columnconfigure(0, weight=1)
        self.polje_dugmad_spisak_amortizacija.columnconfigure(1, weight=1)

        self.dugme_izaberi_amortizaciju_iz_spiska = Button(self.polje_dugmad_spisak_amortizacija, text="Izaberi amortizaciju", bg="#5887C2", fg="white", command=self.controller.izabrana_amortizacija)
        self.dugme_izaberi_amortizaciju_iz_spiska.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.dugme_obrisi_amortizaciju_iz_spiska = Button(self.polje_dugmad_spisak_amortizacija, text="Obriši amortizaciju", bg="#ffcbcb", command=self.controller.poruka_brisanje)
        self.dugme_obrisi_amortizaciju_iz_spiska.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_sve_amortizacije.bind("<ButtonRelease-1>", self.controller.izaberi_red_amortizacije)

    def pokreni(self, controller):
        self.controller = controller
        self.amortizacija_frame = LabelFrame(self.master, text="Amortizacija", font=('Helvetica', 12, 'bold'))
        self.amortizacija_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.amortizacija_frame.columnconfigure(0, weight=1)
        self.amortizacija_frame.rowconfigure(0, weight=1)
        self.amortizacija_frame.rowconfigure(1, weight=2)

        tabovi = ttk.Notebook(self.amortizacija_frame)
        tabovi.grid(row=0, column=0, sticky='nsew')

        tab1 = Frame(tabovi)
        tab1.columnconfigure(0, weight=1)
        tab1.rowconfigure(0, weight=1)
        tab2 = Frame(tabovi)
        tab2.columnconfigure(0, weight=1)
        tab2.rowconfigure(1, weight=1)

        tabovi.add(tab1, text="Uradi amortizaciju")
        tabovi.add(tab2, text="Pregled uradjenih amortizacija")

        ''' prvi tab '''
        self.gornji_frame = Frame(tab1)
        self.gornji_frame.grid(row=0, column=0, padx=10, pady=10)
        self.datum_amortizacije_label = Label(self.gornji_frame, text="Unesi datum amortizacije:")
        self.datum_amortizacije_label.grid(row=0, column=0, padx=10, pady=10)
        self.datum_amortizacije = DateEntry(self.gornji_frame, selectmode='day', locale='sr_RS',
                                            date_pattern='dd.MM.yyyy', font='5')
        self.datum_amortizacije.grid(row=0, column=1, padx=10, pady=10)
        self.dugme_uradi = Button(self.gornji_frame, text="Uradi amortizaciju", command=controller.racunaj_amortizaciju, bg="lightblue")
        self.dugme_uradi.grid(row=0, column=2, padx=10, pady=10)

        ''' drugi tab '''
        self.dugme_izaberi_amortizaciju = Button(tab2, text="Izaberi uradjenu amortizaciju", bg="lightblue", command=self.otvori_prozor_spisak_amortizacija)
        self.dugme_izaberi_amortizaciju.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.naziv_amortizacije = Label(tab2, text="", font=("Helvetica", 12, "bold"))
        self.naziv_amortizacije.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="ew")

        ''' tabela '''
        self.tabela_frame = Frame(self.amortizacija_frame)
        self.tabela_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tabela_frame.columnconfigure(0, weight=1)
        self.tabela_frame.rowconfigure(0, weight=1)
        self.tabela_frame.rowconfigure(1, weight=2)
        self.tabela_frame.rowconfigure(2, weight=1)

        self.naslov_amortizacije = Label(self.tabela_frame, text="Izveštaj obračuna amortizacije po kontima", font=('Helvetica', 14))
        self.naslov_amortizacije.grid(row=0, column=0, padx=10, pady=0)
        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_amortizacija = Canvas(self.tabela_frame)
        self.canvas_amortizacija.grid(row=1, column=0, sticky='nsew')
        self.canvas_amortizacija.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_amortizacija = ttk.Treeview(self.canvas_amortizacija)
        self.my_tree_amortizacija.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_amortizacija['columns'] = ("Konto", "Naziv", "Broj", "Nabavna vrednost", "Tekuća amortizacija", "Dosadašnji otpis", "Ukupan otpis", "Sadašnja vrednost")
        self.my_tree_amortizacija.column("#0", width=0, stretch=False)
        self.my_tree_amortizacija.column("Konto", anchor=tk.CENTER, width=10)
        self.my_tree_amortizacija.column("Naziv", anchor=tk.W, minwidth=50)
        self.my_tree_amortizacija.column("Broj", anchor=tk.CENTER, width=10)
        self.my_tree_amortizacija.column("Nabavna vrednost", anchor=tk.E, width=40)
        self.my_tree_amortizacija.column("Tekuća amortizacija", anchor=tk.E, width=40)
        self.my_tree_amortizacija.column("Dosadašnji otpis", anchor=tk.E, width=40)
        self.my_tree_amortizacija.column("Ukupan otpis", anchor=tk.E, width=40)
        self.my_tree_amortizacija.column("Sadašnja vrednost", anchor=tk.E, width=40)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeAmortizacijaScroll = ttk.Scrollbar(self.canvas_amortizacija)
        self.treeAmortizacijaScroll.grid(row=0, column=1, sticky='ns')
        self.treeAmortizacijaScroll.configure(command=self.my_tree_amortizacija.yview)
        self.my_tree_amortizacija.configure(yscrollcommand=self.treeAmortizacijaScroll.set)

        self.my_tree_amortizacija.heading("#0", anchor=tk.W, text="")
        self.my_tree_amortizacija.heading("Konto", anchor=tk.CENTER, text="Konto")
        self.my_tree_amortizacija.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_amortizacija.heading("Broj", anchor=tk.CENTER, text="Broj OS")
        self.my_tree_amortizacija.heading("Nabavna vrednost", anchor=tk.CENTER, text="Nabavna vrednost")
        self.my_tree_amortizacija.heading("Tekuća amortizacija", anchor=tk.CENTER, text="Tekuća amortizacija")
        self.my_tree_amortizacija.heading("Dosadašnji otpis", anchor=tk.CENTER, text="Dosadašnji otpis")
        self.my_tree_amortizacija.heading("Ukupan otpis", anchor=tk.CENTER, text="Ukupan otpis")
        self.my_tree_amortizacija.heading("Sadašnja vrednost", anchor=tk.CENTER, text="Sadašnja vrednost")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_amortizacija.tag_configure('oddrow', background="white")
        self.my_tree_amortizacija.tag_configure('evenrow', background="lightblue")
        self.amortizacija_id = IntVar()

        self.dugme_stampaj = Button(self.tabela_frame, text="Štampa amortizacije", bg="lightblue", command=controller.stampanje_amortizacije)
        self.dugme_stampaj.grid(row=2, column=0, padx=10, pady=10)
