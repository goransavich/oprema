from tkinter import LabelFrame, Frame, ttk
from views.naslovna_lista import NaslovnaLista
from controllers.naslovna_lista_controller import NaslovnaListaController
from views.unos_view import UnosView
from controllers.unos_controller import UnosController
from controllers.amortizacija_controller import AmortizacijaController
from views.amortizacija_view import Amortizacija
from models.amortizacija_model import AmortizacijaModel
from controllers.rashod_controller import RashodController
from models.rashod_model import RashodModel
from views.rashod_view import RashodView


class OsnovnaSredstva:

    def __init__(self, master):
        self.master = master
        osnovna_sredstva_frame = LabelFrame(self.master, text="Osnovna sredstva")
        osnovna_sredstva_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        osnovna_sredstva_frame.columnconfigure(0, weight=1)
        # osnovna_sredstva_frame.columnconfigure(1, weight=1)
        osnovna_sredstva_frame.rowconfigure(0, weight=1)

        tabovi = ttk.Notebook(osnovna_sredstva_frame)
        tabovi.grid(row=0, column=0, sticky='nsew')
        # tabovi.bind('<<NotebookTabChanged>>', self.on_tab_change)

        tab1 = Frame(tabovi)
        tab1.columnconfigure(0, weight=2)
        tab1.columnconfigure(1, weight=1)
        tab1.rowconfigure(0, weight=1)

        tab2 = Frame(tabovi)
        tab2.columnconfigure(0, weight=1)
        tab2.rowconfigure(0, weight=1)

        tab3 = Frame(tabovi)
        tab3.columnconfigure(0, weight=1)
        tab3.rowconfigure(0, weight=1)

        tab4 = Frame(tabovi)
        tab4.columnconfigure(0, weight=1)
        tab4.rowconfigure(0, weight=1)

        tabovi.add(tab1, text="Pregled osnovnih sredstava")
        tabovi.add(tab2, text="Unos osnovnog sredstva")
        tabovi.add(tab3, text="Rashod osnovnog sredstva")
        tabovi.add(tab4, text="Amortizacija")

        ''' Ovo je tabela na naslovnoj strani u kojoj je prikazan spisak opreme '''
        n = NaslovnaListaController(NaslovnaLista(tab1))
        n.start()

        u = UnosController(UnosView(tab2))
        u.start()

        r = RashodController(RashodModel(), RashodView(tab3))
        r.start()

        a = AmortizacijaController(AmortizacijaModel(), Amortizacija(tab4))
        a.start()
