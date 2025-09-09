from tkinter import messagebox
from views.osnovna_sredstva import OsnovnaSredstva
from controllers.keyboard_controller import KeyboardController


class DobavljaciController:

    def __init__(self, model, view):
        self.model = model
        self.view = view
    ''' Pokretanje otvaranja prozora za unos i pregled dobavljaca '''
    def start(self):
        self.view.pokreni(self)

    ''' Nakon unosa podataka u bazu ocistiti polja za novi unos '''
    def ocisti_polja(self):
        self.view.naziv_entry_dobavljac.delete(0, 'end')
        self.view.mesto_entry_dobavljac.delete(0, 'end')

    def spisak_dobavljaca(self):
        return self.model.read()

    ''' Prikaz liste svih dobavljaca iz baze '''
    def list_svi_dobavljaci(self):
        # povezivanje na bazu i preuzimanje dobavljaca iz tabele
        rezultat = self.spisak_dobavljaca()
        count_dobavljaci = 0
        for record in rezultat:

            if count_dobavljaci % 2 == 0:
                self.view.my_tree_svi_dobavljaci.insert(parent='', index='end', iid=record[0], text='', values=(record[1], record[2]), tags=('evenrow',))
            else:
                self.view.my_tree_svi_dobavljaci.insert(parent='', index='end', iid=record[0], text='', values=(record[1], record[2]), tags=('oddrow',))
            count_dobavljaci += 1

    ''' Unos novog dobavljaca - obrada unetih podataka '''
    def unos_dobavljaca(self):
        naziv_dobavljaca = self.view.naziv_entry_dobavljac.get()
        mesto_dobavljaca = self.view.mesto_entry_dobavljac.get()

        # Provera da li su polja za unos prazna
        if naziv_dobavljaca == '' or mesto_dobavljaca == '':
            messagebox.showwarning("Greška", "Morate uneti i naziv i mesto dobavljača!", parent=self.view.prozor_dobavljaci)
        else:
            self.model.insert_dobavljac(naziv_dobavljaca, mesto_dobavljaca)
            # Brisanje entry polja nakon unosa dobavljaca
            self.ocisti_polja()
            # Brisanje tabele zbog azuriranja nove vrste naloga
            self.view.my_tree_svi_dobavljaci.delete(*self.view.my_tree_svi_dobavljaci.get_children())
            self.view.naziv_entry_dobavljac.focus()
            # povezivanje na bazu i prikaz u tabeli
            self.list_svi_dobavljaci()
            OsnovnaSredstva(self.view.master)

    ''' Selektovanje reda u tabeli '''
    def izaberi_red_dobavljaca(self, e):
        # Prvo isprazniti polja
        self.view.naziv_entry_dobavljac.delete(0, 'end')
        self.view.mesto_entry_dobavljac.delete(0, 'end')
        # Uzeti identifikator reda
        selected = self.view.my_tree_svi_dobavljaci.focus()
        # Uzamanje vrednosti iz izabranog reda
        # Mora ovaj try exept jer selektuje i header tabele, a onda vraća grešku out of range
        try:
            values_dobavljaci = self.view.my_tree_svi_dobavljaci.item(selected, 'values')
            # Prikaz vrednosti u entry poljima
            self.view.naziv_entry_dobavljac.insert(0, values_dobavljaci[0])
            self.view.mesto_entry_dobavljac.insert(0, values_dobavljaci[1])

        except IndexError:
            pass

    ''' Izmena naziva ili mesta dobavljaca '''
    def izmeni_dobavljaca(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_svi_dobavljaci.focus()
        if selected:
            promenjen_naziv_dobavljaca = self.view.naziv_entry_dobavljac.get()
            promenjeno_mesto_dobavljaca = self.view.mesto_entry_dobavljac.get()
            self.view.my_tree_svi_dobavljaci.item(selected, values=(promenjen_naziv_dobavljaca, promenjeno_mesto_dobavljaca), )

            ''' Povezivanje na bazu i update dobavljaca 
                ova provera sa if je ako je sve u redu vraca None
            '''
            if self.model.update_dobavljac(promenjen_naziv_dobavljaca, promenjeno_mesto_dobavljaca, selected) is None:
                # Brisanje entry polja nakon azuriranja vrste naloga
                self.ocisti_polja()
                # Brisanje tabele zbog azuriranja nove vrste naloga
                self.view.my_tree_svi_dobavljaci.delete(*self.view.my_tree_svi_dobavljaci.get_children())
                # povezivanje na bazu i prikaz u tabeli
                self.list_svi_dobavljaci()
                OsnovnaSredstva(self.view.master)
            else:
                messagebox.showinfo("Greska", "Hmmmm, nešto nije u redu unosom izmenjenih podataka u bazu!!",
                                    parent=self.view.prozor_dobavljaci)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednog dobavljača!!", parent=self.view.prozor_dobavljaci)

    ''' Brisanje dobavljaca '''
    def obrisi_dobavljaca(self):
        # Brisanje iz tabele treeview
        selected = self.view.my_tree_svi_dobavljaci.focus()
        if selected:
            x = self.view.my_tree_svi_dobavljaci.selection()[0]
            # prvo se proverava da li ovaj dobavljac postoji u nekoj nabavki, ako postoji, ne može da se obrise
            postoji = self.model.dobavljac_postoji_u_nabavci(x)
            if postoji:
                messagebox.showinfo("Greška", "Za odabranog dobavljača postoji urađena nabavka, ne možete ga obrisati!", parent=self.view.prozor_dobavljaci)
            else:
                #self.view.my_tree_svi_dobavljaci.delete(x)
                # Brisanje iz baze podataka
                try:
                    self.model.delete_dobavljac(selected)
                    # Brisanje entry polja nakon brisanja konta
                    self.ocisti_polja()
                    # Brisanje tabele zbog azuriranja nove vrste naloga
                    self.view.my_tree_svi_dobavljaci.delete(*self.view.my_tree_svi_dobavljaci.get_children())
                    # povezivanje na bazu i prikaz u tabeli
                    self.list_svi_dobavljaci()
                    # Pop up sa porukom o obrisanom kontu

                    messagebox.showinfo("Obrisano", "Odabrani dobavljač je obrisan!", parent=self.view.prozor_dobavljaci)
                    OsnovnaSredstva(self.view.master)
                except ValueError:
                    messagebox.showinfo("Greska", "Hmmmm, neka greška prilikom povezivanja na bazu podataka!!", parent=self.view.prozor_dobavljaci)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jednog dobavljača!!", parent=self.view.prozor_dobavljaci)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_naziv(self, event):
        if self.view.naziv_entry_dobavljac.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_dobavljaci)
                self.view.naziv_entry_dobavljac.delete(0, 'end')

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_mesto(self, event):
        if self.view.mesto_entry_dobavljac.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_dobavljaci)
                self.view.mesto_entry_dobavljac.delete(0, 'end')
