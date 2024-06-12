import customtkinter as ctk
from search import SearchWindow
from database_manager import DatabaseManager
from PIL import Image as myImage, ImageTk
from tkinter import Label

class StylingOptions:
    '''Αφορά τις βασικές ρυθμίσεις εμφάνισης'''
    def __init__(self, master):

        self.master = master
        self.styles()
        self.setup_bg_image()
        

    def styles(self):
        #Βασικά στυλ για χρήση εντός της εφαρμογής
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.master.geometry("1000x800")
        self.master.title("MoMA Database")
        #Full screen
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()

        self.master.geometry(f"{width}x{height}")

        self.master.MOMA_FONT_XLG = ("Helvetica", 60)
        self.master.MOMA_FONT_LG = ("Helvetica", 45)
        self.master.MOMA_FONT_MD = ("Helvetica", 30)
        self.master.MOMA_FONT_SM = ("Helvetica", 20)
        self.master.MOMA_FONT_XS = ("Helvetica", 15)
        self.master.MOMA_BG = "#1c1c1c"
        self.master.MOMA_BG_SECONDARY = "#2c2c2c"
        self.master.MOMA_BUTTON_PRIMARY = "#007bff"
        self.master.MOMA_BUTTON_SECONDARY = "#6c757d"

    def setup_bg_image(self):
        #Διαχειρίζεται την εικόνα στο background
        
        ImageInBackground(self.master, '../assets/moma_photo.jpg')
            
        

    
        

    

class ImageInBackground: 
    '''Δημιουργεί εικόνα στο background'''
    def __init__(self, master, img_name): 
        try:
            self.original_image = myImage.open(img_name)
        except ImportError as e:
            print("An error occurred while importing background image resize:", e)

        self.img_copy = self.original_image.copy() 
    
        self.background_image = ImageTk.PhotoImage(self.original_image) 
        self.background = Label(master, image = self.background_image) 
        self.background.pack(fill='both', expand=True) 
        self.background.bind('<Configure>', self.resize_background) 

    def resize_background(self, event): 
        #Αλλάζει το μέγεθος της εικόνας ανάλογα με το μέγεθος του παραθύρου
        new_width = event.width 
        new_height = event.height 
        try:
            self.resized_image = self.img_copy.resize ((new_width, new_height)) 
        except Exception as e:
            print("An error occurred during background image resize:", e)

        self.background_image = ImageTk.PhotoImage(self.resized_image) 

        self.background.configure(image=self.background_image) 


class Main_page_UI:
    '''Η κλάση που δημιουργεί και διαχειρίζεται το interface της αρχικής σελίδας, καθώς και τις διεπαφές με άλλες σελίδες'''
    def __init__(self, app):
        self.app = app
        
        self.init_ui()


    def init_ui(self):
        #Εδώ ουσιαστικά δημιουργείται το UI και γίνονται όλες οι λειτουργίες του γραφικού περοβάλλοντος
        StylingOptions(self.app)
        self.draw_header()
        self.draw_search_buttons()
        self.draw_home_button()
        
        self.app.mainloop()

    #Δημιουργία κεφαλίδας
    def draw_header(self):
        self.header = ctk.CTkLabel(
            self.app, 
            text="Welcome to the MoMA collection Database", 
            font=self.app.MOMA_FONT_MD)
        
        self.header.place(
                    relx=0.5, 
                    rely=0.09,
                    relheight = 0.1,
                    relwidth = 0.8,
                    anchor=ctk.CENTER)
        
        self.line = ctk.CTkFrame(
                            self.app, 
                            height=3, 
                            fg_color=self.app.MOMA_BG_SECONDARY)
        self.line.place(
                    relx=0.5, 
                    rely=0.18, 
                    anchor=ctk.CENTER, 
                    relwidth=1)

   #Δημιουργία των κουμπιών. Περιέχεται και κενό Random Artworks κουμπί ως προσχέδιο.
    def draw_search_buttons(self):
        self.search_button_frame = ctk.CTkFrame(self.app)
        self.search_button_frame.place(
                            relx=0.5, 
                            rely=0.55, 
                            relheight = 0.1,
                            relwidth = 0.5,
                            anchor=ctk.CENTER)

        self.search_button = ctk.CTkButton(
                                        self.search_button_frame, 
                                        text = "Search" , 
                                        command=self.search_button_click,
                                        font=self.app.MOMA_FONT_MD, 
                                        hover_color = 'grey', 
                                        fg_color = 'black')
        self.search_button.pack(fill = ctk.BOTH, expand = 1)

        self.random_button_frame = ctk.CTkFrame(self.app)
        self.random_button_frame.place(
                            relx=0.5, 
                            rely=0.8, 
                            relheight = 0.1,
                            relwidth = 0.5,
                            anchor=ctk.CENTER)

        self.random_button = ctk.CTkButton(
                                        self.random_button_frame, 
                                        text = "Random Artwork" , 
                                        command=self.random_button_click,
                                        font=self.app.MOMA_FONT_MD, 
                                        hover_color = 'grey', 
                                        fg_color = 'black')
        self.random_button.pack(fill = ctk.BOTH, expand = 1)

    #Δημιουργία του Home button
    def draw_home_button(self):
        try:
            self.home_image = myImage.open("../assets/Home_Icon.png")
        except ImportError as e:
            print("An error occurred while importing home image:", e)
        try:
            self.resized_image = self.home_image.resize((35, 35))
            self.home_tn = ctk.CTkImage(self.resized_image)
        except Exception as e:
            print("An error occurred during home image resize:", e)
        
        self.home_button = ctk.CTkButton(
                                        self.app, 
                                        command = self.home_button_click,
                                        text = '',
                                        image = self.home_tn,
                                        width = 35,
                                        height = 35,
                                        hover_color = 'grey',
                                        fg_color = 'transparent'
                                        )
        self.home_button.place(rely = 0.99, relx = 0.99, anchor = 'se')

    #To search button καταστρέφει τα κουμπιά της αρχικής σελίδας και ανοίγει το περιβάλλον αναζήτησης
    def search_button_click(self):
        self.search_button_frame.destroy()
        self.random_button_frame.destroy()
        self.header.destroy()
        self.line.destroy()

        self.connection=DatabaseManager().get_connection()
        SearchWindow(self.app, self.connection)

    def random_button_click(self):
        pass
    
    #Το home button καταστρέφει όλα τα widget και επανεκκινεί το UI.
    def home_button_click(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.init_ui()

class Main_Class:
    '''Η κύρια κλάση του προγράμματος, διαχειρίζεται τις υπόλοιπες διεργασίες'''
    def __init__(self):

        master = ctk.CTk()

        DatabaseManager()
        
        Main_page_UI(master)


        

if __name__ == "__main__":
    '''Κύριο πρόγραμμα'''
    Main_Class()