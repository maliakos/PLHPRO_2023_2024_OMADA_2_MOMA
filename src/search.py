import customtkinter as ctk
from query_manager import QueryManager
from datagrid import DataGrid
from PIL import Image
import math


class SearchWindow:
    def __init__(self, app, conn):
        # Intance helpers
        self.app = app
        self.filters = {
            'Title': {
                'type': 'text',
                'label': 'Title',
                'value': None
            },
            'Artist': {
                'type': 'text',
                'label': 'Artist',
                'value': None
            },
            'Nationality': {
                'type': 'text',
                'label': 'Country',
                'value': None
            },
            'Gender': {
                'type': 'dropdown',
                'label': 'Gender',
                'value': None,
            },
            'Dimensions': {
                'type': 'text',
                'label': 'Dimensions',
                'value': None
            },
            'Date': {
                'type': 'text',
                'label': 'Year of Creation',
                'value': None
            },
            'DateAcquired': {
                'type': 'text',
                'label': 'Year of Acquisition',
                'value': None
            },
            'Medium': {
                'type': 'text',
                'label': 'Medium',
                'value': None
            },
        }
        self.query_manager = QueryManager(conn)
        self.current_page = 0
        self.items_per_page = 25
        self.total_count = 0
        # Initialize Instance Data
        self.artists_data = []
        self.artworks_data = []
        self.artworks_tab = None
        self.artworks_table_frame = None
        # Bootstrap the UI
        self.init_ui()
        self.app.mainloop()

    def init_ui(self):
        self.draw_header()
        self.draw_table_selection_tabs()

    def draw_header(self):
        # Draw a header for the search window and a line underneath it.
        header = ctk.CTkLabel(self.app, text="Search the MOMA Collection", font=self.app.MOMA_FONT_LG)
        header.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        line = ctk.CTkFrame(self.app, height=3, fg_color=self.app.MOMA_BG_SECONDARY)
        line.place(relx=0.5, rely=0.18, anchor=ctk.CENTER, relwidth=1)

    def draw_table_selection_tabs(self):
        filters_tabs = ctk.CTkTabview(self.app)
        filters_tabs.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=0.95, relheight=0.7)
        # Have to ovveride a protected class to change the font size of the tabs
        # source: https://www.reddit.com/r/learnpython/comments/16140qe/help_with_making_tabs_larger_in_customtkinter/
        filters_tabs._segmented_button.configure(font=self.app.MOMA_FONT_MD)

        self.artworks_tab = filters_tabs.add("Artworks")
        self.artworks_data = self.search('Artworks')
        artworks_data, artworks_headers, self.total_count = self.artworks_data
        self.total_pages = len(artworks_data) // self.items_per_page
        artworks_filters_frame = ctk.CTkFrame(self.artworks_tab, fg_color=self.app.MOMA_BG_SECONDARY)
        artworks_filters_frame.place(relwidth=0.2, relheight=1)
        self.draw_artwork_sidebar(artworks_filters_frame)
        # We need a reference to the following to use when refreshing the table.
        # That's the reason we "store" them as instance variables
        self.artworks_table_frame = ctk.CTkFrame(self.artworks_tab)
        self.artworks_table_frame.place(relx=0.2, relwidth=0.8, relheight=1)
        DataGrid(self.artworks_table_frame, artworks_data, artworks_headers)
        page_label = ctk.CTkLabel(self.artworks_tab, text=f"Page {self.current_page + 1}/{self.total_pages}", font=self.app.MOMA_FONT_MD)
        page_label.place(relx=0.5, rely=0.95, anchor=ctk.CENTER)

        # Draw the Artists tab
        artists_tab = filters_tabs.add("Artists")
        self.artists_data = self.search('Artists', -1)
        artists_data, artists_headers, _ = self.artists_data
        DataGrid(artists_tab, artists_data, artists_headers)
        filters_tabs.set("Artworks")

    def refresh_artworks_table(self):
        self.artworks_data = self.search('Artworks')
        artworks_data, artworks_headers, self.total_count = self.artworks_data
        self.artworks_table_frame.destroy()
        self.artworks_table_frame = ctk.CTkFrame(self.artworks_tab)
        self.artworks_table_frame.place(relx=0.2, relwidth=0.8, relheight=1)
        DataGrid(self.artworks_table_frame, artworks_data, artworks_headers)
        page_label = ctk.CTkLabel(self.artworks_tab, text=f"Page {self.current_page + 1}/{self.total_pages}", font=self.app.MOMA_FONT_MD)
        page_label.place(relx=0.5, rely=0.95, anchor=ctk.CENTER)

    def total_pages(self):
        return math.ceil(self.total_count / self.items_per_page)

    def draw_artwork_sidebar(self, sidebar_frame):
        # Create the search filters for the Artworks tab based on the filter valionary
        for key, val in self.filters.items():
            label = ctk.CTkLabel(sidebar_frame, text=val['label'], font=self.app.MOMA_FONT_MD)
            label.pack(pady=(10, 0))
            if val['type'] == 'text':
                self.filters[key]['value'] = ctk.StringVar()
                entry = ctk.CTkEntry(sidebar_frame, textvariable=self.filters[key]['value'], font=self.app.MOMA_FONT_MD)
                entry.pack(pady=(10, 0))
            elif val['type'] == 'dropdown':
                options = ['', 'male', 'female', 'unknown', 'non-binary', 'other', 'transgender', 'trans']
                dropdown = ctk.CTkOptionMenu(master=sidebar_frame, values=options, command=self.handle_gender_change,
                                             font=self.app.MOMA_FONT_MD)
                dropdown.pack(pady=(10, 0))
        # Create a search button
        search_button = ctk.CTkButton(sidebar_frame, text="Search", command=self.refresh_artworks_table, font=self.app.MOMA_FONT_MD)
        search_button.pack(pady=(30, 0))
        # Create a clear button
        clear_button = ctk.CTkButton(sidebar_frame, text="Clear", command=self.clear_filters, font=self.app.MOMA_FONT_MD)
        clear_button.pack(pady=(10, 0))

        pagination_frame = ctk.CTkFrame(sidebar_frame)
        pagination_frame.pack(pady=(30, 0))

        # Open the images and resize them
        next_image = Image.open("../assets/next_icon.png").resize((60, 60))
        prev_image = Image.open("../assets/previous_icon.png").resize((60, 60))
        # Convert the images to CTkImage
        next_image = ctk.CTkImage(next_image)
        prev_image = ctk.CTkImage(prev_image)

        prev_button = ctk.CTkButton(pagination_frame, text='', width=75, height=75, hover_color='#fff',
                                    fg_color='#fff', image=prev_image, command=self.previous_page)
        prev_button.pack(side=ctk.LEFT, padx=(0, 10))
        next_button = ctk.CTkButton(pagination_frame, text='',width=75, height=75,
                                    hover_color='#fff', fg_color='#fff', image=next_image, command=self.next_page)
        next_button.pack(side=ctk.LEFT)

    def clear_filters(self):
        for key, val in self.filters.items():
            if val['value'] is not None:
                self.filters[key]['value'].set('')
        self.refresh_artworks_table()

    def handle_gender_change(self, value):
        self.filters['Gender']['value'] = value

    def build_query_constraints(self):
        constraints = []
        for key, val in self.filters.items():
            if val['value'] is not None and val['value'].get() != '':
                if val['type'] == 'text':
                    constraints.append(f"{key} LIKE '%{val['value'].get()}%'")
                elif val['type'] == 'dropdown':
                    constraints.append(f"{key} = '{val['value']}'")
        return constraints

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        self.refresh_artworks_table()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.refresh_artworks_table()

    def search(self, table='Artists', limit=0):
        if limit == 0:
            limit = self.items_per_page
        constraints = self.build_query_constraints()
        offset = self.current_page * self.items_per_page
        data = self.query_manager.get_search_query(table, constraints, self.items_per_page, offset)
        return data if data else []
