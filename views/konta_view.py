from tkinter import ttk, Label, Frame, Button, LabelFrame, Entry, Canvas, Toplevel
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class KontaView:
    def __init__(self, master):
        self.master = master
        self.prozor_konta = None
        self.list_sva_konta = None
        self.canvas_konta = None
        self.style = None
        self.my_tree_sva_konta = None
        self.treeVrstaScroll = None
        self.entry_polja_konta = None
        self.oznaka_label_konto = None
        self.oznaka_entry_konto = None
        self.naziv_label_konto = None
        self.naziv_entry_konto = None
        self.polje_dugmad_konta = None
        self.dugme_dodaj_konto = None
        self.dugme_izmeni_konto = None
        self.dugme_obrisi_konto = None
        self.dugme_izaberi_konto = None

    def pokreni(self, controller):
        self.prozor_konta = Toplevel(self.master)
        self.prozor_konta.grab_set()
        self.prozor_konta.title("Pregled i unos konta")

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
        self.prozor_konta.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_konta.resizable(False, False)
        self.prozor_konta.columnconfigure(0, weight=1)
        self.prozor_konta.rowconfigure(0, weight=1)
        self.prozor_konta.rowconfigure(1, weight=4)
        self.prozor_konta.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih vrsta naloga - tabela
        self.list_sva_konta = Frame(self.prozor_konta)
        self.list_sva_konta.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_sva_konta.columnconfigure(0, weight=1)
        # list_sve_vrste_naloga.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_konta = Canvas(self.list_sva_konta)
        self.canvas_konta.grid(row=0, column=0, sticky='nsew')
        self.canvas_konta.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_sva_konta = ttk.Treeview(self.canvas_konta)
        self.my_tree_sva_konta.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_sva_konta['columns'] = ("Oznaka", "Naziv")
        self.my_tree_sva_konta.column("#0", width=0, stretch=False)
        self.my_tree_sva_konta.column("Oznaka", anchor=tk.CENTER, width=100)
        self.my_tree_sva_konta.column("Naziv", anchor=tk.W, minwidth=250)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeVrstaScroll = ttk.Scrollbar(self.canvas_konta)
        self.treeVrstaScroll.grid(row=0, column=1, sticky='ns')
        self.treeVrstaScroll.configure(command=self.my_tree_sva_konta.yview)
        self.my_tree_sva_konta.configure(yscrollcommand=self.treeVrstaScroll.set)

        self.my_tree_sva_konta.heading("#0", anchor=tk.W, text="")
        self.my_tree_sva_konta.heading("Oznaka", anchor=tk.CENTER, text="Oznaka")
        self.my_tree_sva_konta.heading("Naziv", anchor=tk.CENTER, text="Naziv")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_sva_konta.tag_configure('oddrow', background="white")
        self.my_tree_sva_konta.tag_configure('evenrow', background="lightblue")

        # Prikaz svih vrsta naloga u tabeli
        controller.list_sva_konta()

        # Drugi frame za entry polje naziv
        self.entry_polja_konta = LabelFrame(self.prozor_konta, text="Unos")
        self.entry_polja_konta.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.entry_polja_konta.columnconfigure(0, weight=1)
        self.entry_polja_konta.columnconfigure(1, weight=2)
        self.entry_polja_konta.columnconfigure(2, weight=1)
        self.entry_polja_konta.columnconfigure(3, weight=1)
        self.entry_polja_konta.rowconfigure(0, weight=1)

        # Label i polje za unos oznake konta
        self.oznaka_label_konto = Label(self.entry_polja_konta, text="Oznaka konta:")
        self.oznaka_label_konto.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.oznaka_entry_konto = Entry(self.entry_polja_konta)
        self.oznaka_entry_konto.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.oznaka_entry_konto.bind("<KeyRelease>", controller.proveri_jezik_oznaka)

        # Label i polje za unos naziva konta
        self.naziv_label_konto = Label(self.entry_polja_konta, text="Naziv konta:")
        self.naziv_label_konto.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.naziv_entry_konto = Entry(self.entry_polja_konta)
        self.naziv_entry_konto.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.naziv_entry_konto.bind("<KeyRelease>", controller.proveri_jezik_naziv)

        # Treci frame za dugmad Dodaj, Izmeni, Obrisi i Izaberi
        self.polje_dugmad_konta = LabelFrame(self.prozor_konta, text="Komande", bg="lightblue")
        self.polje_dugmad_konta.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_konta.rowconfigure(0, weight=1)
        self.polje_dugmad_konta.columnconfigure(0, weight=1)
        self.polje_dugmad_konta.columnconfigure(1, weight=1)
        self.polje_dugmad_konta.columnconfigure(2, weight=1)
        self.polje_dugmad_konta.columnconfigure(3, weight=1)

        self.dugme_dodaj_konto = Button(self.polje_dugmad_konta, text="Dodaj konto", command=controller.unos_konta, bg='#40A2D8', fg='white')
        self.dugme_dodaj_konto.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        # self.dugme_dodaj_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_dodaj_nalog.bind("<ButtonRelease>", self.__proveri_jezik, add='+')

        self.dugme_izmeni_konto = Button(self.polje_dugmad_konta, text="Izmeni konto", command=controller.izmeni_konto, bg="#265073", fg="white")
        self.dugme_izmeni_konto.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        # self.dugme_izmeni_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_izmeni_nalog.bind("<ButtonRelease-1>", self.__proveri_jezik, add='+')

        self.dugme_obrisi_konto = Button(self.polje_dugmad_konta, text="Obriši konto", command=controller.obrisi_konto, bg="#FF6868", fg="white")
        self.dugme_obrisi_konto.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.dugme_izaberi_konto = Button(self.polje_dugmad_konta, text="Očisti polja za unos", command=controller.ocisti_polja)
        self.dugme_izaberi_konto.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_sva_konta.bind("<ButtonRelease-1>", controller.izaberi_red_konta)
