from tkinter import Label
import customtkinter as ctk
from PIL import Image as myImage, ImageTk
import requests
from io import BytesIO


#Ελαφρώς βελτιωμένα μερικά πράγματα, λίγο πιο περίπλοκο με κλάσεις, βοήθησε το https://github.com/TomSchimansky/CustomTkinter/wiki/CTkToplevel
class PopUpWindow(ctk.CTkToplevel):
    def __init__(self, master, data):
        super().__init__(master)
        self.data = data
        self.title(f"Details for {data.get('Title', 'Artwork Details')}")
        self.geometry("1500x1000")
        my_url = data.get('ImageURL', None)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        if my_url:
            try:
                response = requests.get(my_url, headers=headers)
                response.raise_for_status()

                image_content = response.content
                image_data = BytesIO(image_content)
                self.my_img = myImage.open(image_data)
                self.my_img_copy = self.my_img.copy()
                self.moma_image = ImageTk.PhotoImage(self.my_img)

                self.img_label = Label(self, image=self.moma_image, text='')
                self.img_label.place(relx=1, rely=0.5, relwidth=0.5, relheight=1, anchor='e')

                self.img_label.bind('<Configure>', self.resize_background)
                self.create_labels()

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")

            except myImage.UnidentifiedImageError as e:
                print(f"Cannot identify image: {e}")

    def resize_background(self, event):
        '''Αλλάζει το μέγεθος της εικόνας ανάλογα με το μέγεθος του παραθύρου'''
        new_width = event.width
        new_height = event.height

        self.resized_image = self.my_img_copy.resize((new_width, new_height))
        self.moma_image = ImageTk.PhotoImage(self.resized_image)
        self.img_label.configure(image=self.moma_image)

    def create_labels(self):
        labels_info = [
            ('Title', 0.05), ('Artist', 0.15), ('Date', 0.25),
            ('Medium', 0.35), ('Dimensions', 0.45), ('CreditLine', 0.55),
            ('AccessionNumber', 0.65), ('Classification', 0.75),
            ('Department', 0.85), ('DateAcquired', 0.95)
        ]

        for text, rel_y in labels_info:
            label = ctk.CTkLabel(self, text=f"{text}: {self.data.get(text, '-')}", font=("Helvetica", 25), anchor='w', text_color='white')
            label.place(relwidth=0.5, relheight=0.1, anchor='w', relx=0.1, rely=rel_y)
