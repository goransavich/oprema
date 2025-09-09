from tkinter import messagebox
from controllers.keyboard_controller import KeyboardController


class StopeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    ''' Pokretanje otvaranja prozora za unos i pregled amortizacionih stopa '''
    def start(self):
        self.view.pokreni(self)

    ''' Nakon unosa podataka u bazu ocistiti polja za novi unos '''
    def ocisti_polja(self):
        self.view.oznaka_entry_stopa.delete(0, 'end')
        self.view.naziv_entry_stopa.delete(0, 'end')
        self.view.procenat_entry_stopa.delete(0, 'end')

    ''' Prikaz liste svih stopa iz baze '''
    def list_sve_stope(self):
        # povezivanje na bazu i preuzimanje stopa iz tabele
        rezultat = self.model.read()
        count_stope = 0
        for record in rezultat:

            if count_stope % 2 == 0:
                self.view.my_tree_sve_stope.insert(parent='', index='end', iid=record[0], text='',
                                            values=(record[1], record[2], record[3]),
                                            tags=('evenrow',))
            else:
                self.view.my_tree_sve_stope.insert(parent='', index='end', iid=record[0], text='',
                                            values=(record[1], record[2], record[3]),
                                            tags=('oddrow',))
            count_stope += 1

    ''' Unos nove stope - obrada unetih podataka '''
    def unos_stope(self):
        oznaka_stope = self.view.oznaka_entry_stopa.get()
        naziv_stope = self.view.naziv_entry_stopa.get()
        procenat_stope = self.view.procenat_entry_stopa.get()

        # Provera da li su polja za unos prazna
        if oznaka_stope == '' or naziv_stope == '' or procenat_stope == '':
            messagebox.showwarning("Greška", "Morate uneti vrednosti u sva tri polja!", parent=self.view.prozor_stope)
        else:
            #procenat = procenat_stope.replace(',', ".")
            promenjeno = procenat_stope.replace(',', '.')
            # Overwrite the Entrybox content using the widget's own methods
            self.view.procenat_entry_stopa.delete(0, 'end')
            self.view.procenat_entry_stopa.insert(0, promenjeno)

            try:
                float(self.view.procenat_entry_stopa.get())
            except ValueError:
                self.view.procenat_entry_stopa.delete(0, 'end')
                messagebox.showwarning("Greska", "Morate uneti brojeve u polju za amortizacionu stopu!!",
                                       parent=self.view.prozor_stope)
            else:
                # pravljenje dva decimalna mesta
                prom = float(self.view.procenat_entry_stopa.get())
                if prom > 100:
                    messagebox.showwarning("Greska", "Iznos amortizacione stope ne može biti veći od 100!!",
                                           parent=self.view.prozor_stope)
                else:
                    promenjen_broj = "{:.1f}".format(prom)
                    self.model.insert_stopa(oznaka_stope, naziv_stope, promenjen_broj)
                    # Brisanje entry polja nakon unosa stope
                    self.ocisti_polja()
                    # Brisanje tabele zbog azuriranja nove stope
                    self.view.my_tree_sve_stope.delete(*self.view.my_tree_sve_stope.get_children())
                    self.view.oznaka_entry_stopa.focus()
                    # povezivanje na bazu i prikaz u tabeli
                    self.list_sve_stope()

    ''' Selektovanje reda u tabeli '''
    def izaberi_red_stopa(self, e):
        # Prvo isprazniti polja
        self.view.oznaka_entry_stopa.delete(0, 'end')
        self.view.naziv_entry_stopa.delete(0, 'end')
        self.view.procenat_entry_stopa.delete(0, 'end')
        # Uzeti identifikator reda
        selected = self.view.my_tree_sve_stope.focus()
        # Uzamanje vrednosti iz izabranog reda
        # Mora ovaj try exept jer selektuje i header tabele, a onda vraća grešku out of range
        try:
            values_stope = self.view.my_tree_sve_stope.item(selected, 'values')
            # Prikaz vrednosti u entry poljima
            self.view.oznaka_entry_stopa.insert(0, values_stope[0])
            self.view.naziv_entry_stopa.insert(0, values_stope[1])
            self.view.procenat_entry_stopa.insert(0, values_stope[2])
        except IndexError:
            pass

    ''' Izmena oznake, naziva ili procenta stope '''
    def izmeni_stopu(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_sve_stope.focus()
        if selected:
            promenjena_oznaka_stope = self.view.oznaka_entry_stopa.get()
            promenjen_naziv_stope = self.view.naziv_entry_stopa.get()
            promenjen_procenat_stope = self.view.procenat_entry_stopa.get()
            #self.view.my_tree_sve_stope.item(selected, values=(promenjena_oznaka_stope, promenjen_naziv_stope, promenjen_procenat_stope), )

            ''' Povezivanje na bazu i update stope 
                ova provera sa if je ako je sve u redu vraca None
            '''
            promenjeno = promenjen_procenat_stope.replace(',', '.')
            # Overwrite the Entrybox content using the widget's own methods
            self.view.procenat_entry_stopa.delete(0, 'end')
            self.view.procenat_entry_stopa.insert(0, promenjeno)

            try:
                float(self.view.procenat_entry_stopa.get())
            except ValueError:
                self.view.procenat_entry_stopa.delete(0, 'end')
                messagebox.showwarning("Greska", "Morate uneti brojeve u polju za amortizacionu stopu!!",
                                       parent=self.view.prozor_stope)
            else:
                # pravljenje dva decimalna mesta
                prom = float(self.view.procenat_entry_stopa.get())
                if prom > 100:
                    messagebox.showwarning("Greska", "Iznos amortizacione stope ne može biti veći od 100!!",
                                           parent=self.view.prozor_stope)
                else:
                    promenjen_broj = "{:.1f}".format(prom)

                    if self.model.update_stopa(promenjena_oznaka_stope, promenjen_naziv_stope, promenjen_broj, selected) is None:
                        # Brisanje entry polja nakon azuriranja vrste naloga
                        self.ocisti_polja()
                        # Brisanje tabele zbog azuriranja nove vrste naloga
                        self.view.my_tree_sve_stope.delete(*self.view.my_tree_sve_stope.get_children())
                        # povezivanje na bazu i prikaz u tabeli
                        self.list_sve_stope()
                    else:
                        messagebox.showinfo("Greska", "Hmmmm, nešto nije u redu unosom izmenjenih podataka u bazu!!",
                                            parent=self.view.prozor_stope)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednu stopu!!", parent=self.view.prozor_stope)

    ''' Brisanje stope '''
    def obrisi_stopu(self):
        # Brisanje iz tabele treeview
        selected = self.view.my_tree_sve_stope.focus()
        if selected:
            x = self.view.my_tree_sve_stope.selection()[0]
            # prvo se proverava da li stopa dodeljena nekom osnovnom sredstvu, ako jeste - ne moze da se obrise
            postoji = self.model.stopa_postoji_u_osnovnom_sredstvu(x)
            if postoji:
                messagebox.showinfo("Greška", "Odabrana stopa je dodeljena nekom osnovnom sredstvu - ne možete je obrisati", parent=self.view.prozor_stope)
            else:
                #self.view.my_tree_sve_stope.delete(x)
                # Brisanje iz baze podataka
                try:
                    self.model.delete_stopa(selected)
                    # Brisanje entry polja nakon brisanja konta
                    self.ocisti_polja()
                    # Brisanje tabele zbog azuriranja nove vrste naloga
                    self.view.my_tree_sve_stope.delete(*self.view.my_tree_sve_stope.get_children())
                    # povezivanje na bazu i prikaz u tabeli
                    self.list_sve_stope()
                    # Pop up sa porukom o obrisanom kontu
                    messagebox.showinfo("Obrisano", "Odabrana stopa je obrisana!", parent=self.view.prozor_stope)
                except:
                    messagebox.showinfo("Greska", "Hmmmm, neka greška prilikom povezivanja na bazu podataka!!", parent=self.view.prozor_stope)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednu stopu!!", parent=self.view.prozor_stope)

    def pronadji_stopu_po_id(self, id_stopa):
        return self.model.find_stopa(id_stopa)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_oznaka(self, event):
        if self.view.oznaka_entry_stopa.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_stope)
                self.view.oznaka_entry_stopa.delete(0, 'end')

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_naziv(self, event):
        if self.view.naziv_entry_stopa.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_stope)
                self.view.naziv_entry_stopa.delete(0, 'end')
