from tkinter import *
from tkinter.ttk import *

class Table:
    def on_click(self, function):
        self.function = function

    def click(self, event):
        selected = self.table.focus()
        item = self.table.item(selected)['values']
        self.function(item)


    def set_items(self, items):
        # Clear Table
        for item in self.table.get_children():
            self.table.delete(item)

        # Insert Items
        for item in items:
            self.table.insert('', END, values=item)

    def __init__(self, master, row, col, header, width, x, y):
        self.selected_item = None
        self.table = Treeview(master, height=row, columns=header, show='headings')
        self.table.place(x=x, y=y)

        for i in range(col):
            self.table.column(header[i], width=width[i])
            self.table.heading(header[i], text=header[i])

        self.table.bind("<ButtonRelease>", self.click)
