import customtkinter as ctk
from search import SearchWindow
from database_manager import DatabaseManager
from PIL import Image as myImage, ImageTk

class StylingOptions:
    '''Αφορά τις βασικές ρυθμίσεις εμφάνισης'''
    def __init__(self, master):

        self.master = master
        self.styles()
        self.setup_bg_image()

    def styles(self):
        '''Βασικά στυλ για χρήση εντός της εφαρμογής'''
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.master.geometry("1000x800")

        self.master.MOMA_FONT_LG = ("Helvetica", 45)
        self.master.MOMA_FONT_MD = ("Helvetica", 30)
        self.master.MOMA_FONT_SM = ("Helvetica", 20)
        self.master.MOMA_FONT_XS = ("Helvetica", 15)
        self.master.MOMA_BG = "#1c1c1c"
        self.master.MOMA_BG_SECONDARY = "#2c2c2c"
        self.master.MOMA_BUTTON_PRIMARY = "#007bff"
        self.master.MOMA_BUTTON_SECONDARY = "#6c757d"

    def setup_bg_image(self):
        '''Διαχειρίζεται την εικόνα στο background'''
        try:
            resize_frame = ImageInBackground(self.master)
            resize_frame.pack(fill=BOTH, expand=YES)
        except Exception as e:
            print("An error occurred during setup_resize:", e)
        

    

class ImageInBackground(ctk.CTkFrame): 
    '''Δημιουργεί εικόνα στο background με χρήση της Frame'''
    def __init__(self, master): 
  
        ctk.CTkFrame.__init__(self, master) 

        self.or_image = myImage.open("moma_photo.jpg")

        self.img_copy = self.or_image.copy() 

        self.background_image = ImageTk. PhotoImage(self.or_image) 
        self.background = Label(self, image=self.background_image) 
        self.background.pack(fill=BOTH, expand=YES) 
        self.background.bind('<Configure>', self.resize_background) 

    def resize_background(self, event): 
        '''Αλλάζει το μέγεθος της εικόνας ανάλογα με το μέγεθος του παραθύρου'''
        new_width = event.width 
        new_height = event.height 

        self.or_image = self.img_copy.resize ((new_width, new_height)) 

        self.background_image = ImageTk.PhotoImage(self.or_image) 

        self.background.configure(image=self.background_image) 


class Main_Class:
    '''Η κύρια κλάση του προγράμματος, διαχειρίζεται τις υπόλοιπες διεργασίες'''
    def __init__(self):

        master = ctk.CTk()
        
        StylingOptions(master)

        connection=DatabaseManager().get_connection()

        SearchWindow(master, connection)
        



if __name__ == "__main__":
    Main_Class()