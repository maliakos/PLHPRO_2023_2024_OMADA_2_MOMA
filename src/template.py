import customtkinter as ctk
import sqlite3


class MyWindow:
    def __init__(self, app, conn):
        self.app = app
        self.c = conn
        self.init_ui()
        self.app.mainloop()

    def init_ui(self):
        self.button = ctk.CTkButton(master=self.app, text="CTkButton",
                                    command=self.button_function)
        self.button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def button_function(self):
        print("Hello World")

    def do_something_db_related(self):
        artists = self.c.execute("SELECT * FROM artists")
        for artist in artists:
            print(artist)


# Αυτά γίνονται σε άλλο αρχείο στο main.py
# Προσομοίωση του τί θά μας στέλνει γιά να δουλέψουμε στο module μας
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
master = ctk.CTk()
connection = sqlite3.connect('moma.db')
master.geometry("1000x800")
MyWindow(master, connection)
