from tksheet import Sheet


# This class is not a window, its role is to create a data grid and mount it on the frame/window
# that instantiates it passing the data to be displayed and a reference of the frame/window
class DataGrid:

    def __init__(self, master, data, headers):
        self.sheet = None
        self.data = data
        self.headers = headers
        self.master = master
        self.draw_table()

    # This method creates the data grid and mounts it on the frame/window
    def draw_table(self):
        # Create the data grid
        self.sheet = Sheet(self.master,
                           data=self.data,
                           headers=self.headers,
                           width=1600,
                           height=800,
                           theme='dark blue',
                           max_row_height=50,
                           show_row_index=False,
                           )
        self.sheet.enable_bindings("row_select")
        self.sheet.pack(fill='both', expand=True)
