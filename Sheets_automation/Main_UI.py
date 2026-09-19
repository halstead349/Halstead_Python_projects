import tkinter as tk
from tkinter import ttk,messagebox
import sheets_updator as sheets
# import GAccount_handlers


class SheetsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.client = client
        self.current_sheet = None
        self.sheets_list = []
        self.headers = []
        self.row_no = 0
        self.col_no = 0
        
        self.title("Google Sheets Updater")
        self.geometry("500x600")
        self.configure(padx=20, pady=20)
        
        self.create_widgets()
        
    def create_widgets(self):
        # 1. Sheet Link Input
        tk.Label(self, text="1. Google Sheet Link:").pack(anchor="w")
        self.link_entry = tk.Entry(self, width=60)
        self.link_entry.pack(pady=5)
        
        self.fetch_btn1 = tk.Button(self, text="Fetch Sheets", command=self.fetch_sheets)
        self.fetch_btn1.pack(pady=5)
        
        # 3. Dropdown for Sheets
        tk.Label(self, text="2. Select Sheets:").pack(anchor="w", pady=(15, 0))
        self.sheets_var = tk.StringVar()
        self.dropdown_sheets = ttk.Combobox(self, textvariable=self.sheets_var, state="readonly", width=57)
        self.dropdown_sheets.pack(pady=5)
        
        self.fetch_btn2 = tk.Button(self, text="Fetch Headers", command=self.fetch_headers )
        self.fetch_btn2.pack(pady=5)
        
        # 2. Input for Data to Insert for Part number
        tk.Label(self, text="3. Part number:").pack(anchor="w", pady=(15, 0))
        self.part_entry = tk.Entry(self, width=60)
        self.part_entry.pack(pady=5)
        self.fetch_btn3 = tk.Button(self, text="", command=self.fetch_part_cellvalue)
        self.fetch_btn3.pack(padx=5)
        
        # 3. Dropdown for Column Headers
        tk.Label(self, text="4. Select Column Header:").pack(anchor="w", pady=(15, 0))
        self.header_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.header_var, state="readonly", width=57)
        self.dropdown.pack(pady=5)
        self.dropdown.bind("<<ComboboxSelected>>",self.fetch_cellvalue)
        
        # 4. Input for Data to Insert
        tk.Label(self, text="5. Data to Insert (String or Link):").pack(anchor="w", pady=(15, 0))
        self.cell_value = tk.StringVar()
        self.data_entry = tk.Entry(self, width=60, textvariable=self.cell_value)
        self.data_entry.pack(pady=5)
        
        # 5. Next/Submit Button
        self.next_btn = tk.Button(self, text="Next (Insert Data)", bg="lightblue",command=self.update_cell_value)
        self.next_btn.pack(pady=20)
        
    def fetch_sheets(self):
        self.sheets_list = sheets.fetch_sheets(self.link_entry.get())
        self.dropdown_sheets['values'] = self.sheets_list
        
        
    def fetch_headers(self):
        print(self.sheets_var.get())
        self.headers = sheets.fetch_headers(self.link_entry.get(),self.sheets_var.get())
        self.dropdown['values'] = self.headers
        
    def fetch_part_cellvalue(self):
        self.row_no = sheets.fetch_part_rownumber(self.link_entry.get(),self.sheets_var.get(),self.part_entry.get())
        print(self.row_no)
        
    def fetch_cellvalue(self,event):
        self.col_no = self.dropdown.current()
        self.cell_val = sheets.fetch_cellvalues(self.link_entry.get(),self.sheets_var.get(),self.row_no + 1,self.col_no + 1)
        self.cell_value.set(self.cell_val.value)
        
    def update_cell_value(self):
        sheets.update_cell(self.link_entry.get(),self.sheets_var.get(),self.row_no + 1,self.col_no + 1,self.cell_value.get())
        

        
if __name__ == "__main__":
    app = SheetsApp()
    app.mainloop()
    