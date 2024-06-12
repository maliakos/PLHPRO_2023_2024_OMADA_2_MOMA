import customtkinter as ctk
from tkinter import StringVar
from query_manager import QueryManager
from datagrid import DataGrid
from PIL import Image
from CTkToolTip import CTkToolTip
import math


class SearchWindow:
    def __init__(self, app, conn):
        # Intance helpers
        self.app = app
        self.dimension_filters = {
            'min_height': StringVar(),
            'max_height': StringVar(),
            'min_width': StringVar(),
            'max_width': StringVar(),
        }
        self.filters = {
            'Title': {
                'type': 'text',
                'label': 'Title',
                'value': StringVar(),
                'table': 'Artworks',
            },
            'Artist': {
                'type': 'text',
                'label': 'Artist',
                'value': StringVar(),
                'table': 'Artworks',
            },
            'Nationality': {
                'type': 'text',
                'label': 'Nationality',
                'value': StringVar(),
                'table': 'Artists',
            },
            'Gender': {
                'type': 'dropdown',
                'label': 'Gender',
                'value': StringVar(),
                'table': 'Artists',
            },
            'Date': {
                'type': 'text',
                'label': 'Year of Creation',
                'value': StringVar(),
                'table': 'Artworks',
            },
            'DateAcquired': {
                'type': 'text',
                'label': 'Year of Acquisition',
                'value': StringVar(),
                'table': 'Artworks',
            },
            'Medium': {
                'type': 'text',
                'label': 'Medium',
                'value': StringVar(),
                'table': 'Artworks',
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
        artworks_data, artworks_headers, total_count = self.artworks_data
        self.total_count = total_count
        artworks_filters_frame = ctk.CTkScrollableFrame(self.artworks_tab, fg_color=self.app.MOMA_BG_SECONDARY)
        artworks_filters_frame.place(relwidth=0.2, relheight=1)
        self.draw_artwork_sidebar(artworks_filters_frame)
        # We need a reference to the following to use when refreshing the table.
        # That's the reason we "store" them as instance variables
        self.artworks_table_frame = ctk.CTkFrame(self.artworks_tab)
        self.artworks_table_frame.place(relx=0.2, relwidth=0.8, relheight=1)
        DataGrid(self.artworks_table_frame, artworks_data, artworks_headers, 'Artworks')
        page_label = ctk.CTkLabel(self.artworks_tab, text=f"Page {self.current_page + 1}/{self.total_pages}", font=self.app.MOMA_FONT_MD)
        page_label.place(relx=0.5, rely=0.95, anchor=ctk.CENTER)

        # Draw the Artists tab
        artists_tab = filters_tabs.add("Artists")
        self.artists_data = self.search('Artists', -1)
        artists_data, artists_headers, _ = self.artists_data
        DataGrid(artists_tab, artists_data, artists_headers, 'Artists')
        filters_tabs.set("Artworks")

    def refresh_artworks_table(self):
        self.artworks_data = self.search('Artworks')
        artworks_data, artworks_headers, total_count = self.artworks_data
        # Set the current page to 0 if the total count has changed e.g. only when searching and not when changing pages
        if self.total_count != total_count:
            self.current_page = 0
        self.total_count = 0
        self.total_count = total_count
        self.artworks_table_frame.destroy()
        self.artworks_table_frame = ctk.CTkFrame(self.artworks_tab)
        self.artworks_table_frame.place(relx=0.2, relwidth=0.8, relheight=1)
        DataGrid(self.artworks_table_frame, artworks_data, artworks_headers, 'Artworks')
        page_label = ctk.CTkLabel(self.artworks_tab, text=f"Page {self.current_page + 1}/{self.total_pages}", font=self.app.MOMA_FONT_MD)
        page_label.place(relx=0.5, rely=0.95, anchor=ctk.CENTER)

    @property
    def total_pages(self):
        total_count = math.ceil(self.total_count / self.items_per_page)
        return total_count

    def draw_artwork_sidebar(self, sidebar_frame):
        # Create the search filters for the Artworks tab based on the filter dictionary
        for key, val in self.filters.items():
            label = ctk.CTkLabel(sidebar_frame, text=val['label'], font=self.app.MOMA_FONT_MD)
            label.pack(pady=(10, 10))
            if val['type'] == 'text':
                self.filters[key]['value'] = ctk.StringVar()
                entry = ctk.CTkEntry(sidebar_frame, textvariable=self.filters[key]['value'], font=self.app.MOMA_FONT_MD)
                entry.pack(pady=(10, 10))
            elif val['type'] == 'dropdown':
                options = ['', 'male', 'female', 'unknown', 'non-binary', 'other', 'transgender', 'trans']
                dropdown = ctk.CTkOptionMenu(master=sidebar_frame, values=options, command=self.handle_gender_change,
                                             font=self.app.MOMA_FONT_MD,dropdown_font=self.app.MOMA_FONT_MD)
                dropdown.pack(pady=(10, 10))
        self.draw_dimensions_filters(sidebar_frame)
        # Create a search button
        search_button = ctk.CTkButton(sidebar_frame, text="Search", command=self.refresh_artworks_table, font=self.app.MOMA_FONT_MD)
        search_button.pack(pady=(50, 10))
        # Create a clear button
        clear_button = ctk.CTkButton(sidebar_frame, text="Clear", command=self.clear, font=self.app.MOMA_FONT_MD)
        clear_button.pack(pady=(10, 10))

        pagination_frame = ctk.CTkFrame(sidebar_frame)
        pagination_frame.pack(pady=(30, 0))

        # Open the images and resize them
        next_image = Image.open("../assets/next_icon.png").resize((60, 60))
        prev_image = Image.open("../assets/previous_icon.png").resize((60, 60))
        # Convert the images to CTkImage
        next_image = ctk.CTkImage(light_image=next_image, dark_image=next_image, size=(60, 60))
        prev_image = ctk.CTkImage(light_image=prev_image, dark_image=prev_image, size=(60, 60))

        prev_button = ctk.CTkButton(pagination_frame, text='', width=75, height=75, hover_color='#fff',
                                    fg_color='#fff', image=prev_image, command=self.previous_page)
        prev_button.pack(side=ctk.LEFT, padx=(0, 10))
        next_button = ctk.CTkButton(pagination_frame, text='',width=75, height=75,
                                    hover_color='#fff', fg_color='#fff', image=next_image, command=self.next_page)
        next_button.pack(side=ctk.LEFT)

    def draw_dimensions_filters(self, sidebar_frame):
        dimensions = self.query_manager.get_max_min_dimensions_in_cm()
        if dimensions is None or dimensions[0] is None:
            return
        dim = {
            'min_height': int(dimensions[0]) if dimensions[0] is not None else None,
            'max_height': int(dimensions[1]) if dimensions[1] is not None else None,
            'min_width': int(dimensions[2]) if dimensions[2] is not None else None,
            'max_width': int(dimensions[3]) if dimensions[3] is not None else None
        }
        # Min height
        min_height_label = ctk.CTkLabel(sidebar_frame,
                                        text="Min Height",
                                        font=self.app.MOMA_FONT_MD)
        min_height_label.pack(pady=(10, 10))
        CTkToolTip(min_height_label, font=self.app.MOMA_FONT_MD, bg_color='black',
                   message=f"({dim['min_height']} to {dim['max_height'] - 1} cm)")
        min_height_entry = ctk.CTkEntry(sidebar_frame, font=self.app.MOMA_FONT_MD,
                                        textvariable=self.dimension_filters['min_height'])
        min_height_entry.pack(pady=(10, 10))
        # max height
        max_height_label = ctk.CTkLabel(sidebar_frame,
                                        text="Max Height",
                                        font=self.app.MOMA_FONT_MD)
        max_height_label.pack(pady=(10, 10))
        CTkToolTip(max_height_label, font=self.app.MOMA_FONT_MD, bg_color='black',
                   message=f"({dim['min_height'] + 1} to {dim['max_height']} cm)")
        max_height_entry = ctk.CTkEntry(sidebar_frame, font=self.app.MOMA_FONT_MD,
                                        textvariable=self.dimension_filters['max_height'])
        max_height_entry.pack(pady=(10, 10))
        # min width
        min_width_label = ctk.CTkLabel(sidebar_frame,
                                       text="Min Width",
                                       font=self.app.MOMA_FONT_MD)
        min_width_label.pack(pady=(10, 10))
        CTkToolTip(min_width_label, font=self.app.MOMA_FONT_MD, bg_color='black',
                   message=f"({dim['min_width']} to {dim['max_width'] - 1} cm)")


        min_width_entry = ctk.CTkEntry(sidebar_frame, font=self.app.MOMA_FONT_MD,
                                       textvariable=self.dimension_filters['min_width'])
        min_width_entry.pack(pady=(10, 10))
        # max width
        max_width_label = ctk.CTkLabel(sidebar_frame,
                                       text="Max Width",
                                       font=self.app.MOMA_FONT_MD)
        max_width_label.pack(pady=(10, 10))
        CTkToolTip(max_width_label, font=self.app.MOMA_FONT_MD, bg_color='black',
                   message=f"({dim['min_width'] + 1} to {dim['max_width']} cm)")
        max_width_entry = ctk.CTkEntry(sidebar_frame, font=self.app.MOMA_FONT_MD,
                                       textvariable=self.dimension_filters['max_width'])
        max_width_entry.pack(pady=(10, 10))

    def clear(self):
        for key, val in self.filters.items():
            if val['value'] is not None and isinstance(val['value'], StringVar):
                self.filters[key]['value'].set('')
            elif val['value'] is not None and isinstance(val['value'], str):
                self.filters[key]['value'] = ''
        self.refresh_artworks_table()
        self.total_count = 0
        self.current_page = 0

    def handle_gender_change(self, value):
        self.filters['Gender']['value'] = value

    def build_query_constraints(self):
        constraints = []
        for key, val in self.filters.items():
            actual_value = val['value']
            if (actual_value is not None and
                    (isinstance(actual_value, StringVar) and val['value'].get() != '') or
                    (isinstance(actual_value, str) and val['value'] != '')):
                if val['type'] == 'text':
                    constraints.append(f"{val['table']}.{key} LIKE '%{val['value'].get()}%'")
                elif val['type'] == 'dropdown':
                    constraints.append(f"{key} = '{val['value']}'")
        for key, val in self.dimension_filters.items():
            if val is not None and val.get() != '':
                if key == 'min_height' and self.dimension_filters['max_height'].get() != '':
                    constraints.append(f"Height_cm BETWEEN {val.get()} AND {self.dimension_filters['max_height'].get()}")
                elif key == 'min_height':
                    constraints.append(f"Height_cm >= {val.get()}")
                elif key == 'max_height':
                    constraints.append(f"Height_cm <= {val.get()}")
                elif key == 'min_width' and self.dimension_filters['max_width'].get() != '':
                    constraints.append(f"Width_cm BETWEEN {val.get()} AND {self.dimension_filters['max_width'].get()}")
                elif key == 'min_width':
                    constraints.append(f"Width_cm >= {val.get()}")
                elif key == 'max_width':
                    constraints.append(f"Width_cm <= {val.get()}")
        return constraints

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        self.refresh_artworks_table()

    def next_page(self):
        if (self.current_page + 1) < self.total_pages:
            self.current_page += 1
            self.refresh_artworks_table()

    def search(self, table='Artists', limit=0):
        if limit == 0:
            limit = self.items_per_page
        constraints = self.build_query_constraints()
        offset = self.current_page * self.items_per_page
        data = self.query_manager.get_search_query(table, constraints, self.items_per_page, offset)
        return data if data else []
