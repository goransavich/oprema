# Importing tk library
from views.mainwindow import MainWindow
from views.naslov import Naslov
from views.podesavanja import Podesavanja
from views.osnovna_sredstva import OsnovnaSredstva
from tkinter import *

# root window
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=4)

# Definisan glavni prozor
main_window = MainWindow(root)

# Prvi frame - naslov
Naslov(root)

# Drugi frame
Podesavanja(root)

# Treci frame
OsnovnaSredstva(root)

root.mainloop()
