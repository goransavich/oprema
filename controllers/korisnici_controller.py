from tkinter import messagebox
from views.osnovna_sredstva import OsnovnaSredstva
from controllers.keyboard_controller import KeyboardController


class KorisniciController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    ''' Pokretanje otvaranja prozora za unos i pregled korisnika '''
    def start(self):
        self.view.pokreni(self)

    ''' Nakon unosa podataka u bazu ocistiti polja za novi unos '''
    def ocisti_polja(self):
        self.view.oznaka_entry_korisnik.delete(0, 'end')

    ''' Prikaz liste svih stopa iz baze '''
    def list_svi_korisnici(self):
        # povezivanje na bazu i preuzimanje stopa iz tabele
        rezultat = self.model.read()

        count_korisnici = 0
        for record in rezultat:

            if count_korisnici % 2 == 0:
                self.view.my_tree_svi_korisnici.insert(parent='', index='end', iid=record[0], text='',
                                            values=(record[1],),
                                            tags=('evenrow',))
            else:
                self.view.my_tree_svi_korisnici.insert(parent='', index='end', iid=record[0], text='',
                                            values=(record[1],),
                                            tags=('oddrow',))
            count_korisnici += 1

    ''' Unos nove stope - obrada unetih podataka '''
    def unos_korisnika(self):
        oznaka_korisnika = self.view.oznaka_entry_korisnik.get()

        # Provera da li su polja za unos prazna
        if oznaka_korisnika == '':
            messagebox.showwarning("Greška", "Morate popuniti polje!", parent=self.view.prozor_korisnici)
        else:
            self.model.insert_korisnika(oznaka_korisnika)
            # Brisanje entry polja nakon unosa stope
            self.ocisti_polja()
            # Brisanje tabele zbog azuriranja nove stope
            self.view.my_tree_svi_korisnici.delete(*self.view.my_tree_svi_korisnici.get_children())
            self.view.oznaka_entry_korisnik.focus()
            # povezivanje na bazu i prikaz u tabeli
            self.list_svi_korisnici()
            OsnovnaSredstva(self.view.master)

    ''' Selektovanje reda u tabeli '''
    def izaberi_red_korisnik(self, e):
        # Prvo isprazniti polja
        self.view.oznaka_entry_korisnik.delete(0, 'end')
        # Uzeti identifikator reda
        selected = self.view.my_tree_svi_korisnici.focus()
        # Uzamanje vrednosti iz izabranog reda
        # Mora ovaj try exept jer selektuje i header tabele, a onda vraća grešku out of range
        try:
            values_korisnici = self.view.my_tree_svi_korisnici.item(selected, 'values')
            # Prikaz vrednosti u entry poljima
            self.view.oznaka_entry_korisnik.insert(0, values_korisnici[0])
        except IndexError:
            pass

    ''' Izmena oznake mesta '''
    def izmeni_korisnika(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_svi_korisnici.focus()
        if selected:
            x = self.view.my_tree_svi_korisnici.selection()[0]
            pronadjen = self.model.pronadji_korisnika(x)
            if pronadjen[0][1] == "NEDODELJEN":
                messagebox.showinfo("Greska", "Ne možete menjati naziv ove stavke!!",
                                    parent=self.view.prozor_korisnici)
            else:
                promenjena_oznaka_korisnika = self.view.oznaka_entry_korisnik.get()
                self.view.my_tree_svi_korisnici.item(selected, values=(promenjena_oznaka_korisnika,), )

                ''' Povezivanje na bazu i update korisnika 
                    ova provera sa if je ako je sve u redu vraca None
                '''
                if self.model.update_korisnika(promenjena_oznaka_korisnika, selected) is None:
                    # Brisanje entry polja nakon azuriranja korisnika
                    self.ocisti_polja()
                    # Brisanje tabele zbog azuriranja korisnika
                    self.view.my_tree_svi_korisnici.delete(*self.view.my_tree_svi_korisnici.get_children())
                    # povezivanje na bazu i prikaz u tabeli
                    self.list_svi_korisnici()
                    OsnovnaSredstva(self.view.master)
                else:
                    messagebox.showinfo("Greska", "Hmmmm, nešto nije u redu unosom izmenjenih podataka u bazu!!",
                                        parent=self.view.prozor_korisnici)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednog zaposlenog!!", parent=self.view.prozor_korisnici)


    ''' Brisanje mesta '''
    def obrisi_korisnika(self):
        # Brisanje iz tabele treeview
        selected = self.view.my_tree_svi_korisnici.focus()
        if selected:
            x = self.view.my_tree_svi_korisnici.selection()[0]
            ''' ovde ide provera da li je korisnik dodeljen nekom osnovnom sredstvu, ako jeste - ne moze da se brise'''
            pronadjen_korisnik = self.model.korisnik_postoji_u_osnovnom_sredstvu(x)
            if pronadjen_korisnik:
                messagebox.showinfo("Greška", "Ne možete obrisati ovog korisnika, jer ima osnovno sredstvo za koje je zadužen", parent=self.view.prozor_korisnici)
            else:
                pronadjen = self.model.pronadji_korisnika(x)
                if pronadjen[0][1] == "NEDODELJEN":
                    messagebox.showinfo("Greska", "Ne možete obrisati ovu stavku!!",
                                        parent=self.view.prozor_korisnici)
                else:
                    #self.view.my_tree_svi_korisnici.delete(x)
                    # Brisanje iz baze podataka
                    try:
                        self.model.delete_korisnik(selected)
                        # Brisanje entry polja nakon brisanja korisnika
                        self.ocisti_polja()
                        # Brisanje tabele zbog azuriranja korisnika
                        self.view.my_tree_svi_korisnici.delete(*self.view.my_tree_svi_korisnici.get_children())
                        # povezivanje na bazu i prikaz u tabeli
                        self.list_svi_korisnici()
                        # Pop up sa porukom o obrisanom korisniku

                        messagebox.showinfo("Obrisano", "Odabrani zaposleni je obrisan!", parent=self.view.prozor_korisnici)
                        OsnovnaSredstva(self.view.master)
                    except:
                        messagebox.showinfo("Greska", "Hmmmm, neka greška prilikom povezivanja na bazu podataka!!", parent=self.view.prozor_korisnici)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednog zaposlenog!!", parent=self.view.prozor_korisnici)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_oznaka(self, event):
        if self.view.oznaka_entry_korisnik.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_korisnici)
                self.view.oznaka_entry_korisnik.delete(0, 'end')

