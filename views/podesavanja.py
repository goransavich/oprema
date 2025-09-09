from tkinter import Button, LabelFrame
from controllers.dobavljaci_controller import DobavljaciController
from models.dobavljaci_model import DobavljaciModel
from views.dobavljaci_view import DobavljaciView
from controllers.konto_controller import KontoController
from models.konto_model import KontoModel
from views.konta_view import KontaView
from views.stope_view import StopeView
from models.stope_model import StopeModel
from controllers.stope_controller import StopeController
from controllers.mesta_controller import MestaController
from models.mesta_model import MestaModel
from views.mesta_view import MestaView
from controllers.korisnici_controller import KorisniciController
from models.korisnici_model import KorisniciModel
from views.korisnici_view import KorisniciView
from controllers.sistem_controller import SistemController
from models.sistem_model import SistemModel
from views.sistem_view import SistemView

''' Polje sa dugmadima za podesavanja '''


class Podesavanja:
    def otvori_dobavljace(self):
        d = DobavljaciController(DobavljaciModel(), DobavljaciView(self.master))
        d.start()

    def otvori_konto(self):
        k = KontoController(KontoModel(), KontaView(self.master))
        k.start()

    def stope_amortizacije(self):
        s = StopeController(StopeModel(), StopeView(self.master))
        s.start()

    def mesta(self):
        m = MestaController(MestaModel(), MestaView(self.master))
        m.start()

    def korisnici(self):
        kor = KorisniciController(KorisniciModel(), KorisniciView(self.master))
        kor.start()

    def sistem(self):
        sis = SistemController(SistemModel(), SistemView(self.master))
        sis.start()

    def __init__(self, master):
        self.master = master
        self.podesavanja_frame = LabelFrame(text="Podešavanja", bg="#eaf6f6")
        self.podesavanja_frame.grid(row=1, column=0, padx=10, sticky="ew")
        self.dobavljaci = Button(self.podesavanja_frame, text="Dobavljači", command=self.otvori_dobavljace, bg="lightblue")
        self.dobavljaci.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")
        self.konta = Button(self.podesavanja_frame, text="Konta", command=self.otvori_konto, bg="lightblue")
        self.konta.grid(row=0, column=1, pady=10, sticky="w")
        self.stope = Button(self.podesavanja_frame, text="Stope amortizacije", command=self.stope_amortizacije, bg="lightblue")
        self.stope.grid(row=0, column=2, pady=10, sticky="w")
        self.lokacije = Button(self.podesavanja_frame, text="Lokacije", command=self.mesta, bg="lightblue")
        self.lokacije.grid(row=0, column=3, pady=10, sticky="w")
        self.zaposleni = Button(self.podesavanja_frame, text="Korisnici", command=self.korisnici, bg="lightblue")
        self.zaposleni.grid(row=0, column=4, pady=10, sticky="w")
        self.sistem = Button(self.podesavanja_frame, text="Sistem", command=self.sistem, bg="#FFCF81")
        self.sistem.grid(row=0, column=5, padx=(10, 0), pady=10, sticky="w")
