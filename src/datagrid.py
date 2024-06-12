from tksheet import Sheet
from artwork_details import PopUpWindow
from customtkinter import CTkLabel


# This class is not a window, its role is to create a data grid and mount it on the frame/window
# that instantiates it passing the data to be displayed and a reference of the frame/window
class DataGrid:

    def __init__(self, master, data, headers, table_name):
        self.sheet = None
        # Convert the data to a list of lists otherwise an error will be raised
        self.data = [list(row) for row in data]
        self.headers = [header for header in headers]
        self.table_name = table_name
        # Insert a column for the details button
        self.headers.insert(0, 'Details')
        self.data = [['Browse Details', *row] for row in self.data]
        self.master = master
        self.spans = []
        self.draw_table()

    # This method creates the data grid and mounts it on the frame/window
    def draw_table(self):

        #Do not display the ImageURL and , URL columns
        displayed_headers = [header for header in self.headers if header not in ['ImageURL', 'URL']]
        displayed_data = [[data for i, data in enumerate(row) if self.headers[i] not in ['ImageURL', 'URL']] for row in self.data]

        # Create the data grid
        self.sheet = Sheet(self.master,
                           data=displayed_data,
                           headers=displayed_headers,
                           width=1600,
                           height=800,
                           theme='dark blue',
                           max_row_height=50,
                           default_column_width=200,
                           show_row_index=False,
                           )
        self.sheet.enable_bindings()
        self.sheet.highlight_cells(row="all", column=0, bg="#6c757d",
                                       fg="#FFFFFF")
        self.sheet.extra_bindings([("cell_select", self.handle_button_click)])
        self.sheet.set_all_cell_sizes_to_text(True, 350)
        if self.table_name == 'Artworks':
            column_width_corrections = [1,4, 9, 10, 11, 12,13, 14, 15, 16, 17, 18, 19, 20, 21]
            for i in column_width_corrections:
                self.sheet.column_width(i, 200)
        self.sheet.pack(fill='both', expand=True)

    def handle_button_click(self, _):
        row, column = list(self.sheet.get_selected_cells(get_rows=True, get_columns=True))[0]
        if column == 0:
            self.show_details(row)

    def show_details(self, row):
        # Exclude the first element (Details on the grid) from both the headers and the data
        headers = self.headers[1:]
        data = self.data[row][1:]
        # Create a dictionary from the headers and data
        data_dictionary = dict(zip(headers, data))
        PopUpWindow(self.master, data_dictionary)
