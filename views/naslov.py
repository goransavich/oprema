from tkinter import Frame, Label


class Naslov:

    def __init__(self, master):
        self.master = master
        self.naslov = Frame(self.master, bg="#347083")
        self.naslov.grid(column=0, row=0, sticky="ew", padx=10, pady=10)
        self.naslov.columnconfigure(0, weight=1)
        # Definisanje naslova
        self.naslov_label = Label(self.naslov, text="Evidencija osnovnih sredstava", font=("Helvetica", 14), bg="#347083", fg="white")
        self.naslov_label.grid(row=0, column=0, padx=10, pady=20)
