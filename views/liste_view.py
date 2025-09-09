from tkinter import ttk, Label, Button, LabelFrame, Toplevel
from tkcalendar import DateEntry


class ListeView:
    def __init__(self, master):
        self.master = master
        self.liste_frame = None
        self.frame_stampa_ostalo = None
        self.frame_stampa_popisa = None
        self.lista_datuma_za_stampu = None
        self.label_stampa_na_dan = None
        self.padajuca_lista_datuma = None
        self.label_sortirano = None
        self.padajuca_lista_sortirano = None
        self.dugme_stampaj_popis = None
        self.spisak_label = None
        self.vrste_kombo = None
        self.u_periodu_label = None
        self.datum_od = None
        self.datum_do = None
        self.stampa_liste = None

    def pokreni(self, controller):
        self.liste_frame = Toplevel(self.master)
        self.liste_frame.columnconfigure(0, weight=1)
        self.liste_frame.columnconfigure(1, weight=1)
        #self.liste_frame.rowconfigure(0, weight=1)
        window_height = 250
        window_width = 800
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.liste_frame.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.liste_frame.title("Štampanje popisnih listi")
        self.liste_frame.resizable(None, None)

        self.frame_stampa_popisa = LabelFrame(self.liste_frame, text="Štampa popisa")
        self.frame_stampa_popisa.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.lista_datuma_za_stampu = controller.lista_svih_datuma()
        self.label_stampa_na_dan = Label(self.frame_stampa_popisa, text="Štampa na dan:")
        self.label_stampa_na_dan.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.padajuca_lista_datuma = ttk.Combobox(self.frame_stampa_popisa, values=self.lista_datuma_za_stampu, state='readonly')
        self.padajuca_lista_datuma.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.padajuca_lista_datuma.current(len(self.lista_datuma_za_stampu)-1)

        lista_sortirano = ['po inventarnom broju', 'po korisnicima', 'po kancelarijama', 'po amort.grupama']
        self.label_sortirano = Label(self.frame_stampa_popisa, text="Sortirano po:")
        self.label_sortirano.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.padajuca_lista_sortirano = ttk.Combobox(self.frame_stampa_popisa, values=lista_sortirano, state='readonly')
        self.padajuca_lista_sortirano.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.padajuca_lista_sortirano.current(0)

        self.dugme_stampaj_popis = Button(self.frame_stampa_popisa, text="Štampaj", command=controller.stampa_popisne_liste, bg='lightblue')
        self.dugme_stampaj_popis.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.frame_stampa_ostalo = LabelFrame(self.liste_frame, text="Ostale liste")
        self.frame_stampa_ostalo.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.spisak_label = Label(self.frame_stampa_ostalo, text="Spisak:")
        self.spisak_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.vrste_kombo = ttk.Combobox(self.frame_stampa_ostalo, values=['Nabavljene opreme', 'Rashodovane opreme'], state='readonly')
        self.vrste_kombo.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='ew')
        self.vrste_kombo.current(0)

        self.u_periodu_label = Label(self.frame_stampa_ostalo, text="U periodu:")
        self.u_periodu_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.datum_od = DateEntry(self.frame_stampa_ostalo, selectmode='day', locale='sr_RS', date_pattern='dd.MM.yyyy', font='5', justify="center")
        self.datum_od.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.datum_do = DateEntry(self.frame_stampa_ostalo, selectmode='day', locale='sr_RS', date_pattern='dd.MM.yyyy',
                                  font='5', justify="center")
        self.datum_do.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.stampa_liste = Button(self.frame_stampa_ostalo, text="Štampaj", bg='lightblue', command=controller.stampa_ostalo)
        self.stampa_liste.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

        self.stampaj_pomocnu_knjigu_os = Button(self.liste_frame, text="Pomoćna knjiga osnovnih sredstava", bg="#5887C2", fg="white", command=controller.pomocna_knjiga_os)
        self.stampaj_pomocnu_knjigu_os.grid(row=1, column=0, padx=10, pady=10, sticky='ew')