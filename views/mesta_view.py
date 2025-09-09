from tkinter import ttk, Label, Frame, Button, LabelFrame, Entry, Canvas, Toplevel
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class MestaView:
    def __init__(self, master):
        self.master = master
        self.prozor_mesta = None
        self.list_sva_mesta = None
        self.canvas_mesta = None
        self.my_tree_sva_mesta = None
        self.style = None
        self.treeMestaScroll = None
        self.entry_polja_mesta = None
        self.oznaka_label_mesto = None
        self.oznaka_entry_mesto = None
        self.polje_dugmad_mesta = None
        self.dugme_dodaj_mesto = None
        self.dugme_izmeni_mesto = None
        self.dugme_obrisi_mesto = None
        self.dugme_izaberi_mesto = None

    # Prelazak fokusa na sledeci entry
    @staticmethod
    def focus_next_window(event):
        event.widget.tk_focusNext().focus()

    def pokreni(self, controller):
        self.prozor_mesta = Toplevel(self.master)
        self.prozor_mesta.grab_set()
        self.prozor_mesta.title("Pregled i unos kancelarija i mesta gde se nalazi oprema")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        dimenzije = DimenzijeProzora(screen_width, screen_height)
        window_width = dimenzije.odredi_sirinu_mesto()
        window_height = dimenzije.odredi_visinu_mesto()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        if self.master.winfo_screenheight() < 800:
            y_cordinate = 0
        else:
            y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.prozor_mesta.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_mesta.resizable(False, False)
        self.prozor_mesta.columnconfigure(0, weight=1)
        self.prozor_mesta.rowconfigure(0, weight=1)
        self.prozor_mesta.rowconfigure(1, weight=4)
        self.prozor_mesta.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih vrsta naloga - tabela
        self.list_sva_mesta = Frame(self.prozor_mesta)
        self.list_sva_mesta.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_sva_mesta.columnconfigure(0, weight=1)
        # list_sve_vrste_naloga.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_mesta = Canvas(self.list_sva_mesta)
        self.canvas_mesta.grid(row=0, column=0, sticky='nsew')
        self.canvas_mesta.columnconfigure(0, weight=1)
        # canvas_vrste_naloga.rowconfigure(0, weight=1)
        # Definisanje tabele sa proknjizenim nalozima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3")
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        # Kreiranje canvasa za tabelu jer ne moze scroll bar da ide na Frame ili LabelFrame
        self.my_tree_sva_mesta = ttk.Treeview(self.canvas_mesta)
        self.my_tree_sva_mesta.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree_sva_mesta['columns'] = "Oznaka"
        self.my_tree_sva_mesta.column("#0", width=0, stretch=False)
        self.my_tree_sva_mesta.column("Oznaka", anchor=tk.CENTER, width=100)

        # Kreiranje vertikalnog scroll bara za tabelu
        self.treeMestaScroll = ttk.Scrollbar(self.canvas_mesta)
        self.treeMestaScroll.grid(row=0, column=1, sticky='ns')
        self.treeMestaScroll.configure(command=self.my_tree_sva_mesta.yview)
        self.my_tree_sva_mesta.configure(yscrollcommand=self.treeMestaScroll.set)

        self.my_tree_sva_mesta.heading("#0", anchor=tk.W, text="")
        self.my_tree_sva_mesta.heading("Oznaka", anchor=tk.CENTER, text="Oznaka")

        # Odredjivanje boje u redovima tabele - bela i plava, parni i neparni red
        self.my_tree_sva_mesta.tag_configure('oddrow', background="white")
        self.my_tree_sva_mesta.tag_configure('evenrow', background="lightblue")

        # Prikaz svih vrsta naloga u tabeli
        controller.list_sva_mesta()

        # Drugi frame za entry polje
        self.entry_polja_mesta = LabelFrame(self.prozor_mesta, text="Unos")
        self.entry_polja_mesta.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.entry_polja_mesta.rowconfigure(0, weight=1)

        # Label i polje za unos oznake stope
        self.oznaka_label_mesto = Label(self.entry_polja_mesta, text="Oznaka mesta:")
        self.oznaka_label_mesto.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.oznaka_entry_mesto = Entry(self.entry_polja_mesta)
        self.oznaka_entry_mesto.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.oznaka_entry_mesto.bind("<Return>", self.focus_next_window)
        self.oznaka_entry_mesto.bind("<KeyRelease>", controller.proveri_jezik_oznaka, add="+")

        # Treci frame za dugmad Dodaj, Izmeni, Obrisi i Izaberi
        self.polje_dugmad_mesta = LabelFrame(self.prozor_mesta, text="Komande", bg="lightblue")
        self.polje_dugmad_mesta.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_mesta.rowconfigure(0, weight=1)
        self.polje_dugmad_mesta.columnconfigure(0, weight=1)
        self.polje_dugmad_mesta.columnconfigure(1, weight=1)
        self.polje_dugmad_mesta.columnconfigure(2, weight=1)
        self.polje_dugmad_mesta.columnconfigure(3, weight=1)

        self.dugme_dodaj_mesto = Button(self.polje_dugmad_mesta, text="Dodaj mesto", command=controller.unos_mesto, bg='#40A2D8', fg='white')
        self.dugme_dodaj_mesto.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        # self.dugme_dodaj_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_dodaj_nalog.bind("<ButtonRelease>", self.__proveri_jezik, add='+')

        self.dugme_izmeni_mesto = Button(self.polje_dugmad_mesta, text="Izmeni mesto", command=controller.izmeni_mesto, bg="#265073", fg="white")
        self.dugme_izmeni_mesto.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        # self.dugme_izmeni_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_izmeni_nalog.bind("<ButtonRelease-1>", self.__proveri_jezik, add='+')

        self.dugme_obrisi_mesto = Button(self.polje_dugmad_mesta, text="Obriši mesto", command=controller.obrisi_mesto, bg="#FF6868", fg="white")
        self.dugme_obrisi_mesto.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.dugme_izaberi_mesto = Button(self.polje_dugmad_mesta, text="Očisti polja za unos", command=controller.ocisti_polja)
        self.dugme_izaberi_mesto.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_sva_mesta.bind("<ButtonRelease-1>", controller.izaberi_red_mesto)
