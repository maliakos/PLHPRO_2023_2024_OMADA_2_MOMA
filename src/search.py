import customtkinter as ctk
from database_manager import DatabaseManager
from query_manager import QueryManager


class SearchWindow:
    def __init__(self, app, conn):
        self.app = app
        self.query_manager = QueryManager(conn)
        self.init_ui()
        self.filters = {'Artists': {}, 'Artworks': {}}
        self.app.mainloop()

    def init_ui(self):
        self.draw_header()
        self.draw_table_selection_button()

    def draw_header(self):
        # Draw a header for the search window and a line underneath it.
        header = ctk.CTkLabel(self.app, text="Search the MOMA Collection", font=self.app.MOMA_FONT_LG)
        header.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        line = ctk.CTkFrame(self.app, height=3, fg_color=self.app.MOMA_BG_SECONDARY)
        line.place(relx=0.5, rely=0.18, anchor=ctk.CENTER, relwidth=1)

    def draw_table_selection_button(self):
        # Options for table selection
        table_selection_frame = ctk.CTkFrame(self.app)
        table_selection_frame.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        table_selection_label = ctk.CTkLabel(table_selection_frame, text="Select a table to search:",
                                             font=self.app.MOMA_FONT_MD)
        table_selection_label.pack(side=ctk.LEFT, padx=(0, 10))

        options = ['Artworks', 'Artists']
        dropdown = ctk.CTkSegmentedButton(table_selection_frame, values=options, command=self.draw_filters_dropdown,
                                          font=self.app.MOMA_FONT_MD)
        dropdown.pack(side=ctk.RIGHT)

    def draw_filters_dropdown(self,table_name):

        # Options for Artwork search
        artwork_options = [
            {'name': 'Title', 'type': 'text'},
            {'name': 'Artist', 'type': 'text'},
            {'name': 'Medium', 'type': 'text'},
            {'name': 'Classification', 'type': 'text'}
        ]
        # Options for Artwork search
        artist_options = [
            {'name': 'DisplayName', 'type': 'text'},
            {'name': 'Nationality', 'type': 'distinct'},
            {'name': 'Gender', 'type': 'distinct'}
            ]
        # Check which table is selected and set the options accordingly
        match table_name:
            case 'Artworks':
                options = artwork_options
            case 'Artists':
                options = artist_options
            case _:
                options = []
        # We will render all the filters in this frame
        filters_frame = ctk.CTkFrame(self.app)
        filters_frame.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        for i, option in enumerate(options):
            # Create a label for the filter
            label = ctk.CTkLabel(filters_frame, text=option['name'], font=self.app.MOMA_FONT_MD)
            padding = len(option['name']) + 2
            label.grid(row=0, column=i*2, pady=(10, 0))
            # Create an entry for the filter
            self.filters[table_name][option['name']] = {}
            element = None
            if option['type'] == 'text':
                element = ctk.CTkEntry(filters_frame)
                element.grid(row=1, column=i*2, pady=(0, padding))
            elif option['type'] == 'distinct':
                data = self.query_manager.get_distinct(table_name, option['name'])
                element = ctk.CTkComboBox(filters_frame, values=data, font=self.app.MOMA_FONT_SM)
                element.grid(row=1, column=i*2, pady=(0, padding))
            # Store the value of the filter
            self.filters[table_name][option['name']].update({'element': element})
            # Store the value of the filter
            self.filters[table_name][option['name']].update({'element': element})

    def search(self):
        pass


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
