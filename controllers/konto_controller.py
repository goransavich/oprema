from tkinter import messagebox
from views.osnovna_sredstva import OsnovnaSredstva
from controllers.keyboard_controller import KeyboardController


class KontoController:

    def __init__(self, model, view):
        self.model = model
        self.view = view
    ''' Pokretanje otvaranja prozora za unos i pregled konta '''
    def start(self):
        self.view.pokreni(self)

    ''' Nakon unosa podataka u bazu ocistiti polja za novi unos '''
    def ocisti_polja(self):
        self.view.oznaka_entry_konto.delete(0, 'end')
        self.view.naziv_entry_konto.delete(0, 'end')

    ''' Prikaz liste svih konta iz baze '''
    def list_sva_konta(self):
        # povezivanje na bazu i preuzimanje konta iz tabele
        rezultat = self.model.read()
        if rezultat is not None:
            count_konta = 0
            for record in rezultat:
                if count_konta % 2 == 0:
                    self.view.my_tree_sva_konta.insert(parent='', index='end', iid=record[0], text='', values=(record[1], record[2]), tags=('evenrow',))
                else:
                    self.view.my_tree_sva_konta.insert(parent='', index='end', iid=record[0], text='', values=(record[1], record[2]), tags=('oddrow',))
                count_konta += 1

    ''' Unos novog konta - obrada unetih podataka '''
    def unos_konta(self):
        oznaka_konta = self.view.oznaka_entry_konto.get()
        naziv_konta = self.view.naziv_entry_konto.get()

        # Provera da li su polja za unos prazna
        if oznaka_konta == '' or naziv_konta == '':
            messagebox.showwarning("Greška", "Morate uneti i oznaku i naziv konta!", parent=self.view.prozor_konta)
        else:
            self.model.insert_konto(oznaka_konta, naziv_konta)
            # Brisanje entry polja nakon unosa konta
            self.ocisti_polja()
            # Brisanje tabele zbog azuriranja nove vrste naloga
            self.view.my_tree_sva_konta.delete(*self.view.my_tree_sva_konta.get_children())
            self.view.oznaka_entry_konto.focus()
            # povezivanje na bazu i prikaz u tabeli
            self.list_sva_konta()
            OsnovnaSredstva(self.view.master)

    ''' Selektovanje reda u tabeli '''
    def izaberi_red_konta(self, e):
        # Prvo isprazniti polja
        self.view.oznaka_entry_konto.delete(0, 'end')
        self.view.naziv_entry_konto.delete(0, 'end')
        # Uzeti identifikator reda
        selected = self.view.my_tree_sva_konta.focus()
        # Uzamanje vrednosti iz izabranog reda
        # Mora ovaj try exept jer selektuje i header tabele, a onda vraća grešku out of range
        try:
            values_konta = self.view.my_tree_sva_konta.item(selected, 'values')
            # Prikaz vrednosti u entry poljima
            self.view.oznaka_entry_konto.insert(0, values_konta[0])
            self.view.naziv_entry_konto.insert(0, values_konta[1])

        except IndexError:
            pass

    ''' Izmena oznake ili naziva konta   OVDE UVESTI PROVERU DA LI POSTOJI OPREMA KOJA IMA OVAJ KONTO, AKO IMA ONDA SE NE MENJA OZNAKA'''
    def izmeni_konto(self):
        # Uzeti identifikator reda
        selected = self.view.my_tree_sva_konta.focus()
        if selected:
            promenjena_oznaka_konta = self.view.oznaka_entry_konto.get()
            promenjen_naziv_konta = self.view.naziv_entry_konto.get()
            self.view.my_tree_sva_konta.item(selected, values=(promenjena_oznaka_konta, promenjen_naziv_konta), )

            ''' Povezivanje na bazu i update dobavljaca 
                ova provera sa if je ako je sve u redu vraca None
            '''
            if self.model.update_konto(promenjena_oznaka_konta, promenjen_naziv_konta, selected) is None:
                # Brisanje entry polja nakon azuriranja vrste naloga
                self.ocisti_polja()
                # Brisanje tabele zbog azuriranja nove vrste naloga
                self.view.my_tree_sva_konta.delete(*self.view.my_tree_sva_konta.get_children())
                # povezivanje na bazu i prikaz u tabeli
                self.list_sva_konta()
                OsnovnaSredstva(self.view.master)
            else:
                messagebox.showinfo("Greska", "Hmmmm, nešto nije u redu unosom izmenjenih podataka u bazu!!",
                                    parent=self.view.prozor_konta)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedan konto!!", parent=self.view.prozor_konta)

    ''' Brisanje konto  OVDE UVESTI PROVERU DA LI POSTOJI OPREMA SA TIM KONTOM, AKO IMA NE MOZE SE BRISATI TAJ KONTO'''
    def obrisi_konto(self):
        # Brisanje iz tabele treeview
        selected = self.view.my_tree_sva_konta.focus()
        if selected:
            x = self.view.my_tree_sva_konta.selection()[0]
            # prvo se proverava da li je ovaj ovaj konto dodeljen nekom osnovnom sredstvu, ako jeste - ne moze da se obrise
            #self.view.my_tree_sva_konta.delete(x)
            pronadjen = self.model.konto_postoji_u_osnovnom_sredstvu(x)
            if pronadjen:
                messagebox.showinfo("Greška", "Odabrani konto je dodeljen nekom osnovnom sredstvu pa se ne može obrisati!", parent=self.view.prozor_konta)
            else:
                # Brisanje iz baze podataka
                try:
                    self.model.delete_konto(selected)
                    # Brisanje entry polja nakon brisanja konta
                    self.ocisti_polja()
                    # Brisanje tabele zbog azuriranja nove vrste naloga
                    self.view.my_tree_sva_konta.delete(*self.view.my_tree_sva_konta.get_children())
                    # povezivanje na bazu i prikaz u tabeli
                    self.list_sva_konta()
                    # Pop up sa porukom o obrisanom kontu
                    messagebox.showinfo("Obrisano", "Odabrani konto je obrisan!", parent=self.view.prozor_konta)
                    OsnovnaSredstva(self.view.master)
                except ValueError:
                    messagebox.showinfo("Greska", "Hmmmm, neka greška prilikom povezivanja na bazu podataka!!", parent=self.view.prozor_konta)
        else:
            messagebox.showinfo("Greska", "Hmmmm, niste odabrali ni jedan konto!!", parent=self.view.prozor_konta)

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_oznaka(self, event):
        if self.view.oznaka_entry_konto.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_konta)
                self.view.oznaka_entry_konto.delete(0, 'end')

    # Provera koja tastatura se koristi za unos, ako je cirilica vratiti upozorenje, jer mogu samo da se unose latinicna slova- zbog stampe PDF
    def proveri_jezik_naziv(self, event):
        if self.view.naziv_entry_konto.get() != '':
            ucitaj_kontrolu = KeyboardController()
            if ucitaj_kontrolu.check_language():
                messagebox.showwarning("Greška", "Za unos koristite latinična slova!!",
                                       parent=self.view.prozor_konta)
                self.view.naziv_entry_konto.delete(0, 'end')
