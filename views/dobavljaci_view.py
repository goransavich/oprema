from tkinter import ttk, Label, Frame, Button, LabelFrame, Entry, Canvas, Toplevel
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class DobavljaciView:
    def __init__(self, master):
        self.master = master
        self.prozor_dobavljaci = None
        self.list_svi_dobavljaci = None
        self.canvas_vrste_naloga = None
        self.style = None
        self.my_tree_svi_dobavljaci = None
        self.treeVrstaScroll = None
        self.entry_polja_dobavljaci = None
        self.naziv_label_dobavljaci = None
        self.naziv_entry_dobavljac = None
        self.mesto_label_dobavljaci = None
        self.mesto_entry_dobavljac = None
        self.polje_dugmad_dobavljaci = None
        self.dugme_dodaj_dobavljaca = None
        self.dugme_izmeni_dobavljaca = None
        self.dugme_obrisi_dobavljaca = None
        self.dugme_izaberi_dobavljaca = None

    def pokreni(self, controller):
        self.prozor_dobavljaci = Toplevel(self.master)
        self.prozor_dobavljaci.grab_set()
        self.prozor_dobavljaci.title("Pregled i unos dobavljača")

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
        self.prozor_dobavljaci.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_dobavljaci.resizable(False, False)
        self.prozor_dobavljaci.columnconfigure(0, weight=1)
        self.prozor_dobavljaci.rowconfigure(0, weight=1)
        self.prozor_dobavljaci.rowconfigure(1, weight=4)
        self.prozor_dobavljaci.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih vrsta naloga - tabela
        self.list_svi_dobavljaci = Frame(self.prozor_dobavljaci)
        self.list_svi_dobavljaci.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_svi_dobavljaci.columnconfigure(0, weight=1)
        # list_sve_vrste_naloga.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_vrste_naloga = Canvas(self.list_svi_dobavljaci)
        self.canvas_vrste_naloga.grid(row=0, column=0, sticky='nsew')
        self.canvas_vrste_naloga.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_svi_dobavljaci = ttk.Treeview(self.canvas_vrste_naloga)
        self.my_tree_svi_dobavljaci.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_svi_dobavljaci['columns'] = ("Naziv", "Mesto")
        self.my_tree_svi_dobavljaci.column("#0", width=0, stretch=False)
        self.my_tree_svi_dobavljaci.column("Naziv", anchor=tk.CENTER, width=300)
        self.my_tree_svi_dobavljaci.column("Mesto", anchor=tk.CENTER, minwidth=120)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeVrstaScroll = ttk.Scrollbar(self.canvas_vrste_naloga)
        self.treeVrstaScroll.grid(row=0, column=1, sticky='ns')
        self.treeVrstaScroll.configure(command=self.my_tree_svi_dobavljaci.yview)
        self.my_tree_svi_dobavljaci.configure(yscrollcommand=self.treeVrstaScroll.set)

        self.my_tree_svi_dobavljaci.heading("#0", anchor=tk.W, text="")
        self.my_tree_svi_dobavljaci.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree_svi_dobavljaci.heading("Mesto", anchor=tk.CENTER, text="Mesto")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_svi_dobavljaci.tag_configure('oddrow', background="white")
        self.my_tree_svi_dobavljaci.tag_configure('evenrow', background="lightblue")

        # Prikaz svih vrsta naloga u tabeli
        controller.list_svi_dobavljaci()

        # Drugi frame za entry polje naziv
        self.entry_polja_dobavljaci = LabelFrame(self.prozor_dobavljaci, text="Unos")
        self.entry_polja_dobavljaci.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.entry_polja_dobavljaci.columnconfigure(0, weight=1)
        self.entry_polja_dobavljaci.columnconfigure(1, weight=2)
        self.entry_polja_dobavljaci.columnconfigure(2, weight=1)
        self.entry_polja_dobavljaci.columnconfigure(3, weight=1)
        self.entry_polja_dobavljaci.rowconfigure(0, weight=1)

        # Label i polje za unos naziva dobavljaca
        self.naziv_label_dobavljaci = Label(self.entry_polja_dobavljaci, text="Naziv dobavljača:")
        self.naziv_label_dobavljaci.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.naziv_entry_dobavljac = Entry(self.entry_polja_dobavljaci)
        self.naziv_entry_dobavljac.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.naziv_entry_dobavljac.bind("<KeyRelease>", controller.proveri_jezik_naziv)

        # Label i polje za unos mesta dobavljaca
        self.mesto_label_dobavljaci = Label(self.entry_polja_dobavljaci, text="Mesto dobavljača:")
        self.mesto_label_dobavljaci.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.mesto_entry_dobavljac = Entry(self.entry_polja_dobavljaci)
        self.mesto_entry_dobavljac.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.mesto_entry_dobavljac.bind("<KeyRelease>", controller.proveri_jezik_mesto)

        # Treci frame za dugmad Dodaj, Izmeni, Obrisi i Izaberi
        self.polje_dugmad_dobavljaci = LabelFrame(self.prozor_dobavljaci, text="Komande", bg="lightblue")
        self.polje_dugmad_dobavljaci.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_dobavljaci.rowconfigure(0, weight=1)
        self.polje_dugmad_dobavljaci.columnconfigure(0, weight=1)
        self.polje_dugmad_dobavljaci.columnconfigure(1, weight=1)
        self.polje_dugmad_dobavljaci.columnconfigure(2, weight=1)
        self.polje_dugmad_dobavljaci.columnconfigure(3, weight=1)

        self.dugme_dodaj_dobavljaca = Button(self.polje_dugmad_dobavljaci, text="Dodaj dobavljača", command=controller.unos_dobavljaca, bg='#40A2D8', fg='white')
        self.dugme_dodaj_dobavljaca.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        # self.dugme_dodaj_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_dodaj_nalog.bind("<ButtonRelease>", self.__proveri_jezik, add='+')

        self.dugme_izmeni_dobavljaca = Button(self.polje_dugmad_dobavljaci, text="Izmeni dobavljača", command=controller.izmeni_dobavljaca, bg="#265073", fg="white")
        self.dugme_izmeni_dobavljaca.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        # self.dugme_izmeni_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_izmeni_nalog.bind("<ButtonRelease-1>", self.__proveri_jezik, add='+')

        self.dugme_obrisi_dobavljaca = Button(self.polje_dugmad_dobavljaci, text="Obriši dobavljača", command=controller.obrisi_dobavljaca, bg="#FF6868", fg="white")
        self.dugme_obrisi_dobavljaca.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.dugme_izaberi_dobavljaca = Button(self.polje_dugmad_dobavljaci, text="Očisti polja za unos", command=controller.ocisti_polja)
        self.dugme_izaberi_dobavljaca.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_svi_dobavljaci.bind("<ButtonRelease-1>", controller.izaberi_red_dobavljaca)
