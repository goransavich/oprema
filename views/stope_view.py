from tkinter import ttk, Label, Frame, Button, LabelFrame, Entry, Canvas, Toplevel
from controllers.dimenzije_prozora import DimenzijeProzora
import tkinter as tk


class StopeView:
    def __init__(self, master):
        self.master = master
        self.prozor_stope = None
        self.list_sve_stope = None
        self.canvas_stope = None
        self.style = None
        self.my_tree_sve_stope = None
        self.treeVrstaScroll = None
        self.entry_polja_stope = None
        self.oznaka_label_stopa = None
        self.oznaka_entry_stopa = None
        self.naziv_label_stopa = None
        self.naziv_entry_stopa = None
        self.procenat_label_stopa = None
        self.procenat_entry_stopa = None
        self.polje_dugmad_stopa = None
        self.dugme_dodaj_stopa = None
        self.dugme_izmeni_stopa = None
        self.dugme_obrisi_stopa = None
        self.dugme_izaberi_stopu = None

    # Prelazak fokusa na sledeci entry
    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()

    def pokreni(self, controller):
        self.prozor_stope = Toplevel(self.master)
        self.prozor_stope.grab_set()
        self.prozor_stope.title("Pregled i unos stope amortizacije prema Nomenklaturi")

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
        self.prozor_stope.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.prozor_stope.resizable(False, False)
        self.prozor_stope.columnconfigure(0, weight=1)
        self.prozor_stope.rowconfigure(0, weight=1)
        self.prozor_stope.rowconfigure(1, weight=4)
        self.prozor_stope.rowconfigure(2, weight=3)

        # Prvi frame za spisak svih vrsta naloga - tabela
        self.list_sve_stope = Frame(self.prozor_stope)
        self.list_sve_stope.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.list_sve_stope.columnconfigure(0, weight=1)
        self.list_sve_stope.rowconfigure(0, weight=1)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_stope = Canvas(self.list_sve_stope)
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
        controller.list_sve_stope()

        # Drugi frame za entry polje
        self.entry_polja_stope = LabelFrame(self.prozor_stope, text="Unos")
        self.entry_polja_stope.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.entry_polja_stope.columnconfigure(0, weight=1)
        self.entry_polja_stope.columnconfigure(1, weight=2)
        self.entry_polja_stope.columnconfigure(2, weight=1)
        self.entry_polja_stope.columnconfigure(3, weight=1)
        self.entry_polja_stope.rowconfigure(0, weight=1)

        # Label i polje za unos oznake stope
        self.oznaka_label_stopa = Label(self.entry_polja_stope, text="Oznaka stope:")
        self.oznaka_label_stopa.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.oznaka_entry_stopa = Entry(self.entry_polja_stope)
        self.oznaka_entry_stopa.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.oznaka_entry_stopa.bind("<Return>", self.focus_next_window)
        self.oznaka_entry_stopa.bind("<KeyRelease>", controller.proveri_jezik_oznaka, add="+")

        # Label i polje za unos naziva stope
        self.naziv_label_stopa = Label(self.entry_polja_stope, text="Naziv amortizacione stope:")
        self.naziv_label_stopa.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.naziv_entry_stopa = Entry(self.entry_polja_stope)
        self.naziv_entry_stopa.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.naziv_entry_stopa.bind("<Return>", self.focus_next_window)
        self.naziv_entry_stopa.bind("<KeyRelease>", controller.proveri_jezik_naziv, add="+")

        # Label i polje za unos iznosa stope
        self.procenat_label_stopa = Label(self.entry_polja_stope, text="Amortizaciona stopa (%):")
        self.procenat_label_stopa.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.procenat_entry_stopa = Entry(self.entry_polja_stope)
        self.procenat_entry_stopa.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.procenat_entry_stopa.bind("<Return>", self.focus_next_window)

        # Treci frame za dugmad Dodaj, Izmeni, Obrisi i Izaberi
        self.polje_dugmad_stopa = LabelFrame(self.prozor_stope, text="Komande", bg="lightblue")
        self.polje_dugmad_stopa.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.polje_dugmad_stopa.rowconfigure(0, weight=1)
        self.polje_dugmad_stopa.columnconfigure(0, weight=1)
        self.polje_dugmad_stopa.columnconfigure(1, weight=1)
        self.polje_dugmad_stopa.columnconfigure(2, weight=1)
        self.polje_dugmad_stopa.columnconfigure(3, weight=1)

        self.dugme_dodaj_stopa = Button(self.polje_dugmad_stopa, text="Dodaj stopu", command=controller.unos_stope, bg='#40A2D8', fg='white')
        self.dugme_dodaj_stopa.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        # self.dugme_dodaj_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_dodaj_nalog.bind("<ButtonRelease>", self.__proveri_jezik, add='+')

        self.dugme_izmeni_stopa = Button(self.polje_dugmad_stopa, text="Izmeni stopu", command=controller.izmeni_stopu, bg="#265073", fg="white")
        self.dugme_izmeni_stopa.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        # self.dugme_izmeni_nalog.bind("<Return>", self.__proveri_jezik, add='+')
        # self.dugme_izmeni_nalog.bind("<ButtonRelease-1>", self.__proveri_jezik, add='+')

        self.dugme_obrisi_stopa = Button(self.polje_dugmad_stopa, text="Obriši stopu", command=controller.obrisi_stopu, bg="#FF6868", fg="white")
        self.dugme_obrisi_stopa.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.dugme_izaberi_stopu = Button(self.polje_dugmad_stopa, text="Očisti polja za unos", command=controller.ocisti_polja)
        self.dugme_izaberi_stopu.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        # Selektovanje reda iz tabele klikom na slog
        self.my_tree_sve_stope.bind("<ButtonRelease-1>", controller.izaberi_red_stopa)
