from tkinter import Toplevel, ttk, Button, Label, StringVar


class SistemView:
    def __init__(self, master):
        self.master = master

    def pokreni(self, controller):
        self.prozor_sistem = Toplevel()
        self.prozor_sistem.grab_set()
        self.prozor_sistem.title("Podešavanje sistema")
        self.prozor_sistem.geometry("800x150")
        self.prozor_sistem.resizable(False, False)
        self.prozor_sistem.columnconfigure(0, weight=1)
        self.prozor_sistem.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.prozor_sistem)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.tab_backup_podataka = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_backup_podataka, text='Backup podataka')

        # ************************************* Tab 1 Unos novog korisnika ********************************* #
        self.button_backup = Button(self.tab_backup_podataka, text="Sačuvaj podatke", bg='lightblue', command=controller.cuvanje_podataka)
        self.button_backup.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.datum_poslednjeg_bekapa = StringVar()
        controller.poslednji_bekap()
        self.obavestenje = Label(self.tab_backup_podataka,
                                 text="Datum poslednjeg backup-a:  " + self.datum_poslednjeg_bekapa.get())
        self.obavestenje.grid(row=0, column=2, padx=10, pady=10)
