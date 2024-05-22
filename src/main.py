import customtkinter as ctk
from search import SearchWindow
from database_manager import DatabaseManager



class main_func:
    def __init__(self):
        # Αυτά γίνονται σε άλλο αρχείο στο main.py
        # Προσομοίωση του τί θά μας στέλνει γιά να δουλέψουμε στο module μας
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        master = ctk.CTk()
        master.geometry("1000x800")

        # Add custom font sizes /background colors to use throughout the app
        master.MOMA_FONT_LG = ("Helvetica", 45)
        master.MOMA_FONT_MD = ("Helvetica", 30)
        master.MOMA_FONT_SM = ("Helvetica", 20)
        master.MOMA_FONT_XS = ("Helvetica", 15)
        master.MOMA_BG = "#1c1c1c"
        master.MOMA_BG_SECONDARY = "#2c2c2c"
        master.MOMA_BUTTON_PRIMARY = "#007bff"
        master.MOMA_BUTTON_SECONDARY = "#6c757d"

        connection=DatabaseManager().get_connection()
        SearchWindow(master, connection)
        



if __name__ == "__main__":
    main_func()