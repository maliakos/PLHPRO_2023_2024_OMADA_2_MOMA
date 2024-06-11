from tkinter import Label
import customtkinter as ctk
from PIL import Image as myImage, ImageTk
import requests
from io import BytesIO


class pop_up_window:
    def __init__(self):
        master = ctk.CTk()
        master.geometry("1000x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        my_url = "https://www.moma.org/media/W1siZiIsIjUyNzUzMSJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDEwMjR4MTAyNFx1MDAzZSJdXQ.jpg?sha=0b3e1b840debe461"
        #Έτρωγα άκυρο στο request για την εικόνα, γι'αυτό το από κάτω
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        try:
            self.create_labels(master)
            self.response = requests.get(my_url, headers=headers)
            self.response.raise_for_status()

            self.image_content = self.response.content
            self.image_data = BytesIO(self.image_content)
            self.my_img = myImage.open(self.image_data)
            self.my_img_copy = self.my_img.copy()
            self.moma_image = ImageTk.PhotoImage(self.my_img)
            # Σόρρυ για τα Label αλλά η ctk μου έχει βγάλει ππροβλήματα με τις εικόνες
            self.img_label = Label(master, image=self.moma_image, text = '')
            self.img_label.place(relx = 1, rely = 0.5 , relwidth = .5, relheight = 1 , anchor = 'e')

            self.img_label.bind('<Configure>', self.resize_background) 
            

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")

        except myImage.UnidentifiedImageError as e:
            print(f"Cannot identify image: {e}")

        master.mainloop()
        
    #Αυτό το ξεπατήκωσα από το ImageinBackground της main.py
    def resize_background(self, event): 
        '''Αλλάζει το μέγεθος της εικόνας ανάλογα με το μέγεθος του παραθύρου'''
        new_width = event.width 
        new_height = event.height 

        self.resized_image = self.my_img_copy.resize ((new_width, new_height)) 

        self.moma_image = ImageTk.PhotoImage(self.resized_image) 

        self.img_label.configure(image=self.moma_image) 
    #Στο άλλο αρχείο το έχω βελτιωμένο το label craetion
    def create_labels(self, master):
        
        self.label1 = ctk.CTkLabel(master, text = 'Title:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label1.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.05)

        self.label2 = ctk.CTkLabel(master, text = 'Artist:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label2.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.15)

        self.label3 = ctk.CTkLabel(master, text = 'Date:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label3.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.25)

        self.label4 = ctk.CTkLabel(master, text = 'Medium:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label4.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.35)

        self.label5 = ctk.CTkLabel(master, text = 'Dimensions:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label5.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.45)
    
        self.label6 = ctk.CTkLabel(master, text = 'CreditLine:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label6.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.55)

        self.label7 = ctk.CTkLabel(master, text = 'AccessionNumber:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label7.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.65)

        self.label8 = ctk.CTkLabel(master, text = 'Classification:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label8.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.75)

        self.label9 = ctk.CTkLabel(master, text = 'Department:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label9.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.85)

        self.label10 = ctk.CTkLabel(master, text = 'DateAcquired:', font = ("Helvetica", 25), anchor = 'w', text_color = 'white')
        self.label10.place(relwidth = 0.5, relheight = 0.1, anchor = 'w', relx = 0, rely = 0.95)



if __name__ == "__main__":
    pop_up_window()