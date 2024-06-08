from tksheet import Sheet

class DataGrid:
    def __init__(self, master, conn, per_page=25 ):
        self.master = master
        self.conn = conn
        self.init_ui()

    def init_ui(self):
        self.draw_header()
        self.draw_table()

    def draw_header(self):
        # Draw a header for the search window and a line underneath it.
        header = ctk.CTkLabel(self.master, text="MOMA Collection", font=self.app.MOMA_FONT_LG)
        header.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        line = ctk.CTkFrame(self.app, height=3, fg_color=self.app.MOMA_BG_SECONDARY)
        line.place(relx=0.5, rely=0.18, anchor=ctk.CENTER, relwidth=1)

    def draw_table(self):
        sheet = Sheet(self.app)
        sheet.enable_bindings(("single_select", "row_select", "column_width_resize", "arrowkeys", "right_click_popup_menu",
                               "rc_select", "rc_insert_row", "rc_delete_row", "copy", "cut", "paste", "delete",
                               "undo", "edit_cell"))
        sheet.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=0.8, relheight=0.6)
        sheet.headers([f"Column {i}" for i in range(1, 6)], index='both', height=30, align='center')
        sheet.set_sheet_data([[f"Row {i}, Col {j}" for j in range(1, 6)] for i in range(1, 6)])