from tkinter import messagebox
from views.osnovna_sredstva import OsnovnaSredstva
from controllers.keyboard_controller import KeyboardController


class MestaController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    ''' Pokretanje otvaranja prozora za unos i pregled amortizacionih stopa '''
    def start(self):
        self.view.pokreni(self)

    ''' Nakon unosa podataka u bazu ocistiti polja za novi unos '''
    def ocisti_polja(self):
        self.view.oznaka_entry_mesto.delete(0, 'end')

    ''' Prikaz liste svih stopa iz baze '''
    def list_sva_mesta(self):
        # povezivanje na bazu i preuzimanje stopa iz tabele
        rezultat = self.model.read()
        count_mesta = 0
        for record in rezultat:

            if count_mesta % 2 == 0:
                self.view.my_tree_sva_mesta.insert(parent='', index='end', iid=record[0], text='',
                                            values=(record[1],),
                                            tags=('evenrow',))
            else:
                self.view.my_tree_sva_mesta.insert(parent='', index='end', iid=record[0], text='',
                                            values=(record[1],),
                                            tags=('oddrow',))
            count_mesta += 1

    ''' Unos nove stope - obrada unetih podataka '''
    def unos_mesto(self):
        oznaka_mesta = self.view.oznaka_entry_mesto.get()

        # Provera da li su polja za unos prazna
        if oznaka_mesta == '':
            messagebox.showwarning("Greška", "Morate popuniti polje!", parent=self.view.prozor_mesta)
        else:
            self.model.insert_mesto(oznaka_mesta)
            # Brisanje entry polja nakon unosa stope
            self.ocisti_polja()
            # Brisanje tabele zbog azuriranja nove stope
            self.view.my_tree_sva_mesta.delete(*self.view.my_tree_sva_mesta.get_children())
            self.view.oznaka_entry_mesto.focus()
            # povezivanje na bazu i prikaz u tabeli
            self.list_sva_mesta()
            OsnovnaSredstva(self.view.master)

    ''' Selektovanje reda u tabeli '''
    def izaberi_red_mesto(self, e):
        # Prvo isprazniti polja
        self.view.oznaka_entry_mesto.delete(0, 'end')
        # Uzeti identifikator reda
        selected = self.view.my_tree_sva_mesta.focus()
        # Uzamanje vrednosti iz izabranog reda
        # Mora ovaj try exept jer selektuje i header tabele, a onda vraća grešku out of range
        try:
            values_stope = self.view.my_tree_sva_mesta.item(selected, 'values')
            # Prikaz vrednosti u entry poljima
            self.view.oznaka_entry_mesto.insert(0, values_stope[0])
        except IndexError:
            pass

    ''' Izmena oznake mesta '''
    def izmeni_mesto(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_sva_mesta.focus()
        if selected:
            x = self.view.my_tree_sva_mesta.selection()[0]
            pronadjen = self.model.pronadji_mesto(x)
            if pronadjen[0][1] == "NEDODELJEN":
                messagebox.showinfo("Greska", "Ne možete menjati naziv ove stavke!!",
                                    parent=self.view.prozor_mesta)
            else:
                promenjena_oznaka_mesta = self.view.oznaka_entry_mesto.get()
                self.view.my_tree_sva_mesta.item(selected, values=(promenjena_oznaka_mesta,), )

                ''' Povezivanje na bazu i update stope 
                    ova provera sa if je ako je sve u redu vraca None
                '''
                if self.model.update_mesto(promenjena_oznaka_mesta, selected) is None:
                    # Brisanje entry polja nakon azuriranja vrste naloga
                    self.ocisti_polja()
                    # Brisanje tabele zbog azuriranja nove vrste naloga
                    self.view.my_tree_sva_mesta.delete(*self.view.my_tree_sva_mesta.get_children())
                    # povezivanje na bazu i prikaz u tabeli
                    self.list_sva_mesta()
                    OsnovnaSredstva(self.view.master)
                else:
                    messagebox.showinfo("Greska", "Hmmmm, nešto nije u redu unosom izmenjenih podataka u bazu!!",
                                        parent=self.view.prozor_mesta)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedno mesto!!", parent=self.view.prozor_mesta)

    ''' Brisanje mesta '''
    def obrisi_mesto(self):
        # Brisanje iz tabele treeview
        selected = self.view.my_tree_sva_mesta.focus()
        if selected:
            x = self.view.my_tree_sva_mesta.selection()[0]
            pronadji_lokaciju = self.model.lokacija_postoji_u_osnovnom_sredstvu(x)
            if pronadji_lokaciju:
                messagebox.showinfo("Greška", "Ova lokacija je dodeljena nekom osnovnom sredstvu, ne možete da je obrišete!", parent=self.view.prozor_mesta)
            else:
                pronadjen = self.model.pronadji_mesto(x)
                if pronadjen[0][1] == "NEDODELJEN":
                    messagebox.showinfo("Greska", "Ne možete obrisati ovu stavku!!", parent=self.view.prozor_mesta)
                else:
                    #self.view.my_tree_sva_mesta.delete(x)
                    # Brisanje iz baze podataka
                    try:

                        self.model.delete_mesto(selected)

                        # Brisanje entry polja nakon brisanja konta
                        self.ocisti_polja()
                        # Brisanje tabele zbog azuriranja nove vrste naloga
                        self.view.my_tree_sva_mesta.delete(*self.view.my_tree_sva_mesta.get_children())
                        # povezivanje na bazu i prikaz u tabeli
                        self.list_sva_mesta()
                        # Pop up sa porukom o obrisanom kontu

                        messagebox.showinfo("Obrisano", "Odabrano mesto je obrisano!", parent=self.view.prozor_mesta)
                        OsnovnaSredstva(self.view.master)

                    except:
                        messagebox.showinfo("Greska", "Hmmmm, neka greška prilikom povezivanja na bazu podataka!!", parent=self.view.prozor_mesta)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedno mesto!!", parent=self.view.prozor_mesta)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_oznaka(self, event):
        if self.view.oznaka_entry_mesto.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_korisnici)
                self.view.oznaka_entry_mesto.delete(0, 'end')
