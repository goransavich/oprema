from tkinter import ttk, Label, Frame, Button, LabelFrame, Entry, Canvas, Toplevel
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class KorisniciView:
    def __init__(self, master):
        self.master = master
        self.prozor_korisnici = None
        self.list_svi_korisnici = None
        self.canvas_korisnici = None
        self.my_tree_svi_korisnici = None
        self.style = None
        self.treeKorisniciScroll = None
        self.entry_polja_korisnik = None
        self.oznaka_label_korisnik = None
        self.oznaka_entry_korisnik = None
        self.polje_dugmad_korisnici = None
        self.dugme_dodaj_korisnika = None
        self.dugme_izmeni_korisnika = None
        self.dugme_obrisi_korisnika = None
        self.dugme_izaberi_korisnika = None

    # Prelazak fokusa na sledeci entry
    @staticmethod
    def focus_next_window(event):
        event.widget.tk_focusNext().focus()

    def pokreni(self, controller):
        self.prozor_korisnici = Toplevel(self.master)
        self.prozor_korisnici.grab_set()
        self.prozor_korisnici.title("Pregled i unos zaposlenih koji su zaduženi za opremu")

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
        self.prozor_korisnici.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_korisnici.resizable(False, False)
        self.prozor_korisnici.columnconfigure(0, weight=1)
        self.prozor_korisnici.rowconfigure(0, weight=1)
        self.prozor_korisnici.rowconfigure(1, weight=4)
        self.prozor_korisnici.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih zaposlenih - tabela
        self.list_svi_korisnici = Frame(self.prozor_korisnici)
        self.list_svi_korisnici.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_svi_korisnici.columnconfigure(0, weight=1)
        # list_sve_vrste_naloga.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_korisnici = Canvas(self.list_svi_korisnici)
        self.canvas_korisnici.grid(row=0, column=0, sticky='nsew')
        self.canvas_korisnici.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_svi_korisnici = ttk.Treeview(self.canvas_korisnici)
        self.my_tree_svi_korisnici.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_svi_korisnici['columns'] = ("Naziv")
        self.my_tree_svi_korisnici.column("#0", width=0, stretch=False)
        self.my_tree_svi_korisnici.column("Naziv", anchor=tk.CENTER, width=100)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeKorisniciScroll = ttk.Scrollbar(self.canvas_korisnici)
        self.treeKorisniciScroll.grid(row=0, column=1, sticky='ns')
        self.treeKorisniciScroll.configure(command=self.my_tree_svi_korisnici.yview)
        self.my_tree_svi_korisnici.configure(yscrollcommand=self.treeKorisniciScroll.set)

        self.my_tree_svi_korisnici.heading("#0", anchor=tk.W, text="")
        self.my_tree_svi_korisnici.heading("Naziv", anchor=tk.CENTER, text="Naziv")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_svi_korisnici.tag_configure('oddrow', background="white")
        self.my_tree_svi_korisnici.tag_configure('evenrow', background="lightblue")

        # Prikaz svih korisnika u tabeli
        controller.list_svi_korisnici()

        # Drugi frame za entry polje
        self.entry_polja_korisnik = LabelFrame(self.prozor_korisnici, text="Unos")
        self.entry_polja_korisnik.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.entry_polja_korisnik.rowconfigure(0, weight=1)

        # Label i polje za unos oznake stope
        self.oznaka_label_korisnik = Label(self.entry_polja_korisnik, text="Ime i prezime zaposlenog:")
        self.oznaka_label_korisnik.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.oznaka_entry_korisnik = Entry(self.entry_polja_korisnik)
        self.oznaka_entry_korisnik.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.oznaka_entry_korisnik.bind("<KeyRelease>", controller.proveri_jezik_oznaka)
        self.oznaka_entry_korisnik.bind("<Return>", self.focus_next_window)
        # self.naziv_entry_dobavljac.bind("<KeyRelease>", self.__proveri_jezik)

        # Treci frame za dugmad Dodaj, Izmeni, Obrisi i Izaberi
        self.polje_dugmad_korisnici = LabelFrame(self.prozor_korisnici, text="Komande", bg="lightblue")
        self.polje_dugmad_korisnici.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_korisnici.rowconfigure(0, weight=1)
        self.polje_dugmad_korisnici.columnconfigure(0, weight=1)
        self.polje_dugmad_korisnici.columnconfigure(1, weight=1)
        self.polje_dugmad_korisnici.columnconfigure(2, weight=1)
        self.polje_dugmad_korisnici.columnconfigure(3, weight=1)

        self.dugme_dodaj_korisnika = Button(self.polje_dugmad_korisnici, text="Dodaj zaposlenog", command=controller.unos_korisnika, bg='#40A2D8', fg='white')
        self.dugme_dodaj_korisnika.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        # self.dugme_dodaj_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_dodaj_nalog.bind("<ButtonRelease>", self.__proveri_jezik, add='+')

        self.dugme_izmeni_korisnika = Button(self.polje_dugmad_korisnici, text="Izmeni ime ili prezime zaposlenog", command=controller.izmeni_korisnika, bg="#265073", fg="white")
        self.dugme_izmeni_korisnika.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        # self.dugme_izmeni_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_izmeni_nalog.bind("<ButtonRelease-1>", self.__proveri_jezik, add='+')

        self.dugme_obrisi_korisnika = Button(self.polje_dugmad_korisnici, text="Obriši zaposlenog", command=controller.obrisi_korisnika, bg="#FF6868", fg="white")
        self.dugme_obrisi_korisnika.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.dugme_izaberi_korisnika = Button(self.polje_dugmad_korisnici, text="Očisti polja za unos", command=controller.ocisti_polja)
        self.dugme_izaberi_korisnika.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_svi_korisnici.bind("<ButtonRelease-1>", controller.izaberi_red_korisnik)
