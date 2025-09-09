from tkinter import Button, LabelFrame, Frame, ttk, Canvas, Label
import tkinter as tk
from controllers.liste_controller import ListeController
from views.liste_view import ListeView


class NaslovnaLista:
    def __init__(self, master):
        self.master = master
        self.prozor_detalji_os = None
        self.label_naslov = None
        self.inv_broj_label = None
        self.inv_broj = None
        self.naziv_label = None
        self.naziv = None
        self.datum_fakture_label = None
        self.datum_fakture = None
        self.broj_fakture_label = None
        self.broj_fakture = None
        self.naziv_dobavljaca_label = None
        self.naziv_dobavljaca = None
        self.nabavna_vrednost_label = None
        self.nabavna_vrednost = None
        self.otpisana_vrednost_label = None
        self.otpisana_vrednost = None
        self.status_label = None
        self.status = None
        self.konto_label = None
        self.konto = None
        self.stopa_label = None
        self.stopa = None
        self.lokacija_label = None
        self.lokacija = None
        self.pregled_opreme = None
        self.canvas_pregled_opreme = None
        self.style = None
        self.my_tree = None
        self.treeScroll = None
        self.buttons_frame = None
        self.dugme_pregledaj = None
        self.dugme_osvezi_listu = None
        self.id_os = None
        self.detalji_opreme = None
        self.label_inventarni_broj = None
        self.prikazi_inventarni_broj = None
        self.label_naziv = None
        self.prikazi_naziv = None
        self.label_datum_nabavke = None
        self.prikazi_datum_nabavke = None
        self.label_datum_aktiviranja = None
        self.prikazi_datum_aktiviranja = None
        self.label_broj_fakture = None
        self.prikazi_broj_fakture = None
        self.label_naziv_dobavljaca = None
        self.prikazi_naziv_dobavljaca = None
        self.label_nabavna_vrednost = None
        self.prikazi_nabavna_vrednost = None
        self.label_otpisana_vrednost = None
        self.prikazi_otpisana_vrednost = None
        self.label_trenutna_vrednost = None
        self.prikazi_trenutna_vrednost = None
        self.label_status = None
        self.prikazi_status = None
        self.label_konto = None
        self.prikazi_konto = None
        self.label_stopa = None
        self.prikazi_stopa = None
        self.label_lokacija = None
        self.prikazi_lokacija = None
        self.label_zaduzenje = None
        self.prikazi_zaduzenje = None
        self.prozor_izbor_stope = None
        self.prozor_izmena = None
        self.prvi_frame_prozor_stope = None
        self.canvas_stope = None
        self.my_tree_sve_stope = None
        self.treeVrstaScroll = None
        self.drugi_frame_dugme = None
        self.dugme_izaberi_stopu = None
        self.okvir = None
        self.text_inventarni_broj = None
        self.text_broj_pronadji = None
        self.naziv_izmena = None
        self.text_naziv_izmena = None
        self.datum_nabavke_izmena = None
        self.izmena_datum_nabavke = None
        self.broj_fakture_izmena = None
        self.unet_broj_fakture_izmena = None
        self.naziv_dobavljaca_izmena = None
        self.lista_dobavljaca = None
        self.unet_naziv_dobavljaca_izmena = None
        self.nabavna_vrednost_izmena = None
        self.uneta_nabavna_vrednost_izmena = None
        self.otpisana_vrednost_izmena = None
        self.uneta_otpisana_vrednost_izmena = None
        self.spisak_statusa = None
        self.status_label = None
        self.status_label_izmena = None
        self.spisak_konta = None
        self.unet_status_izmena = None
        self.konto_label_izmena = None
        self.unet_konto_izmena = None
        self.stopa_label_izmena = None
        self.izabrana_stopa_izmena = None
        self.dugme_izaberi_stopu_izmena = None
        self.id_izabrane_stope = None
        self.spisak_lokacija = None
        self.lokacija_label_izmena = None
        self.izabrana_lokacija_izmena = None
        self.spisak_zaposlenih = None
        self.zaduzenje_label_izmena = None
        self.izabrano_zaduzenje_izmena = None
        self.dugme_izmeni_os = None
        self.dugme_izmeni = None
        self.dugme_obrisi = None
        self.controller = None
        self.dugme_stampa_popisa = None

    def popisne_liste(self):
        l = ListeController(ListeView(self.master))
        l.start()

    def pokreni(self, controller):
        self.controller = controller
        # Definisanje polja za prikaz liste osnovnih sredstava
        self.pregled_opreme = Frame(self.master)
        self.pregled_opreme.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.pregled_opreme.columnconfigure(0, weight=1)
        self.pregled_opreme.rowconfigure(0, weight=1)
        self.pregled_opreme.grid_propagate(False)

        # Definisanje Canvasa zbog stavljanja Scroll bara - ne moze scroll bar u labelframe vec samo u canvas
        self.canvas_pregled_opreme = Canvas(self.pregled_opreme)
        self.canvas_pregled_opreme.grid(row=0, column=0, sticky='nsew')
        self.canvas_pregled_opreme.columnconfigure(0, weight=1)
        self.canvas_pregled_opreme.rowconfigure(0, weight=1)
        # Definisanje tabele sa osnovnim sredstvima
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25,
                             fieldbackground="d3d3d3", font=(None, 10))
        # Boja selektrovanog reda
        self.style.map('Treeview', background=[('selected', '#347083')])

        self.my_tree = ttk.Treeview(self.canvas_pregled_opreme)
        self.my_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.my_tree['columns'] = ("R.broj", "Inventarni broj", "Naziv", "Datum nabavke", "Nab.vrednost")
        self.my_tree.column("#0", width=0, stretch=False)
        self.my_tree.column("R.broj", anchor=tk.CENTER, width=40)
        self.my_tree.column("Inventarni broj", anchor=tk.CENTER, minwidth=50)
        self.my_tree.column("Naziv", anchor=tk.W, width=400)
        self.my_tree.column("Datum nabavke", anchor=tk.CENTER, minwidth=50)
        self.my_tree.column("Nab.vrednost", anchor=tk.E, width=80)

        self.treeScroll = ttk.Scrollbar(self.canvas_pregled_opreme)
        self.treeScroll.grid(row=0, column=1, sticky='ns')
        self.treeScroll.configure(command=self.my_tree.yview)
        self.my_tree.configure(yscrollcommand=self.treeScroll.set)

        self.my_tree.heading("#0", anchor=tk.W, text="")
        self.my_tree.heading("R.broj", anchor=tk.CENTER, text="R.broj")
        self.my_tree.heading("Inventarni broj", anchor=tk.CENTER, text="Inventarni broj")
        self.my_tree.heading("Naziv", anchor=tk.CENTER, text="Naziv")
        self.my_tree.heading("Datum nabavke", anchor=tk.CENTER, text="Datum nabavke")
        self.my_tree.heading("Nab.vrednost", anchor=tk.CENTER, text="Nab.vrednost")

        # Prikaz svih aktivnih osnovnih sredstava
        self.controller.spisak_opreme()
        self.my_tree.bind("<ButtonRelease-1>", self.controller.pregledaj_detalje_os)
        self.buttons_frame = Frame(self.pregled_opreme)
        self.buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.dugme_osvezi_listu = Button(self.buttons_frame, text="Osveži listu", bg="lightblue", font=('Helvetica', 11), command=self.controller.spisak_opreme)
        self.dugme_osvezi_listu.grid(row=0, column=0, padx=10, pady=10)

        self.dugme_stampa_popisa = Button(self.buttons_frame, text="Štampa popisnih listi", bg="lightblue", font=('Helvetica', 11), command=self.popisne_liste)
        self.dugme_stampa_popisa.grid(row=0, column=1, pady=10)

        ''' Desni prozor na naslovnoj strani gde se prikazuju detalji selektovanog osnovnog sredstva '''
        self.detalji_opreme = LabelFrame(self.master, text="Detalji osnovnog sredstva")
        self.detalji_opreme.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.detalji_opreme.columnconfigure(0, weight=1)
        self.detalji_opreme.columnconfigure(1, weight=3)
        self.detalji_opreme.grid_propagate(False)

        self.label_inventarni_broj = Label(self.detalji_opreme, text="Inventarni broj:", font=('Helvetica', 11))
        self.label_inventarni_broj.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.prikazi_inventarni_broj = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11, 'bold'))
        self.prikazi_inventarni_broj.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.label_naziv = Label(self.detalji_opreme, text="Naziv:", font=('Helvetica', 11))
        self.label_naziv.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.prikazi_naziv = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_naziv.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self.label_datum_nabavke = Label(self.detalji_opreme, text="Datum nabavke:", font=('Helvetica', 11))
        self.label_datum_nabavke.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.prikazi_datum_nabavke = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_datum_nabavke.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        self.label_broj_fakture = Label(self.detalji_opreme, text="Broj fakture:", font=('Helvetica', 11))
        self.label_broj_fakture.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_broj_fakture = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_broj_fakture.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.label_naziv_dobavljaca = Label(self.detalji_opreme, text="Naziv dobavljaca:", font=('Helvetica', 11))
        self.label_naziv_dobavljaca.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_naziv_dobavljaca = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_naziv_dobavljaca.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.label_nabavna_vrednost = Label(self.detalji_opreme, text="Nabavna vrednost:", font=('Helvetica', 11))
        self.label_nabavna_vrednost.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_nabavna_vrednost = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_nabavna_vrednost.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        self.label_otpisana_vrednost = Label(self.detalji_opreme, text="Otpisana vrednost:", font=('Helvetica', 11))
        self.label_otpisana_vrednost.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_otpisana_vrednost = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_otpisana_vrednost.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.label_trenutna_vrednost = Label(self.detalji_opreme, text="Trenutna vrednost:", font=('Helvetica', 11))
        self.label_trenutna_vrednost.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_trenutna_vrednost = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_trenutna_vrednost.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.label_status = Label(self.detalji_opreme, text="Status:", font=('Helvetica', 11))
        self.label_status.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_status = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_status.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        self.label_konto = Label(self.detalji_opreme, text="Konto:", font=('Helvetica', 11))
        self.label_konto.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_konto = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_konto.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

        self.label_stopa = Label(self.detalji_opreme, text="Stopa:", font=('Helvetica', 11))
        self.label_stopa.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.prikazi_stopa = Label(self.detalji_opreme, text="", borderwidth=2, relief="groove", font=('Helvetica', 11))
        self.prikazi_stopa.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

        self.label_lokacija = Label(self.detalji_opreme, text="Lokacija:", font=('Helvetica', 11))
        self.label_lokacija.grid(row=11, column=0, padx=5, pady=5, sticky="w")

        dictionary_lokacije = self.controller.dictionary_svih_lokacija()
        self.spisak_lokacija = self.controller.lista_svih_lokacija(dictionary_lokacije)
        self.prikazi_lokacija = ttk.Combobox(self.detalji_opreme, font=('Helvetica', 11), values=self.spisak_lokacija, justify='center', state='readonly')
        self.prikazi_lokacija.grid(row=11, column=1, padx=5, pady=5, sticky="ew")

        self.label_zaduzenje = Label(self.detalji_opreme, text="Zaduženje:", font=('Helvetica', 11))
        self.label_zaduzenje.grid(row=12, column=0, padx=5, pady=5, sticky="w")

        dictionary_zaposlenih = self.controller.dictionary_svih_zaposlenih()
        self.spisak_zaposlenih = self.controller.lista_svih_zaposlenih(dictionary_zaposlenih)
        self.prikazi_zaduzenje = ttk.Combobox(self.detalji_opreme, font=('Helvetica', 11), values=self.spisak_zaposlenih, justify='center', state='readonly')
        self.prikazi_zaduzenje.grid(row=12, column=1, padx=5, pady=5, sticky="ew")

        self.dugme_izmeni = Button(self.detalji_opreme, text="Izmeni lokaciju ili zaduženje", bg="lightblue", font=('Helvetica', 11), command=controller.izmeni_osnovno_sredstvo)
        self.dugme_izmeni.grid(row=13, column=1, padx=5, pady=(25, 5), sticky='ew')
