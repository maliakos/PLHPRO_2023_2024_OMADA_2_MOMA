import customtkinter as ctk
from database_manager import DatabaseManager


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
        cursor = self.c.cursor()
        cursor.execute("SELECT * FROM artists LIMIT 50")
        rows = cursor.fetchall()
        description = cursor.description
        for row in rows:
            print(row)


    def do_something_db_related(self):
        artists = self.c.execute("SELECT * FROM artists")
        for artist in artists:
            print(artist)


# Αυτά γίνονται σε άλλο αρχείο στο main.py
# Προσομοίωση του τί θά μας στέλνει γιά να δουλέψουμε στο module μας
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
master = ctk.CTk()
master.geometry("1000x800")
connection=DatabaseManager().get_connection()
MyWindow(master, connection)
