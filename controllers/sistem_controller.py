from tkinter import messagebox
from datetime import datetime
import subprocess
import os
import webbrowser


class SistemController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    ''' Pokretanje otvaranja prozora za unos i pregled konta '''

    def start(self):
        self.view.pokreni(self)

    def cuvanje_podataka(self):
        username = 'root'
        password = 'UrLe19023009'
        database = 'oprema'
        now = datetime.now()
        danasnji_datum = now.strftime("%m%d%Y%H%M%S")
        naziv_snimljene_baze = ".\\sacuvano\\sacuvano_oprema" + danasnji_datum + ".sql"

        try:
            with open(naziv_snimljene_baze, 'w') as output:
                c = subprocess.Popen(["C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe", "-u", username, "-p%s" % password, database],
                                 stdout=output, shell=True)

            datum_bekapa = now.strftime('%Y-%m-%d %H:%M:%S')
            self.model.insert_bekap(datum_bekapa)
            messagebox.showinfo("Odlično", "Uspešno su sačuvani podaci! Bekap se nalazi u folderu Sacuvano!", parent=self.view.prozor_sistem)
            path = ".\\sacuvano\\"
            webbrowser.open(os.path.realpath(path))
        except ValueError:
            messagebox.showinfo("Hmmmmm", "Nešto nije u redu sa bekapom!", parent=self.view.prozor_sistem)

    def poslednji_bekap(self):
        try:
            rezultat = self.model.find_last()
            if len(rezultat) == 0:
                self.view.datum_poslednjeg_bekapa.set('Još uvek nije radjen bekap podataka')
            else:
                vreme_poslednjeg_bekapa=rezultat[0][1].strftime("%d.%m.%Y, %H:%M:%S")
                self.view.datum_poslednjeg_bekapa.set(vreme_poslednjeg_bekapa)
        except ValueError:
            messagebox.showinfo("Hmmmmm", "Nešto nije u redu sa bazom podataka!", parent=self.view.prozor_sistem)

