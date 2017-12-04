from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import socket
import configparser
import settings_popup
import menu_frame


class Window(Tk):
    """   главное окно GUI   """
    def __init__(self, master=None):
        Tk.__init__(self)
        self.geometry("900x700")
        self.title("instant messaging client")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        self.frames = {}

        # панель инструментов
        menubar = Menu(self)
        menubar.add_command(label="new tab", command=self.create_new_tab)
        menubar.add_command(label="close current tab", command=self.close_current_tab)
        menubar.add_command(label="settings", command=settings_popup.Settings)
        self.config(menu=menubar)
        self.create_new_tab()


    def create_new_tab(self):
        frame = menu_frame.Menu(self.notebook)
        self.frames[frame.winfo_name()] = frame
        self.notebook.add(frame, text="new tab")
        self.notebook.select(len(self.notebook.tabs())-1)


    def close_current_tab(self):
        self.notebook.forget(self.notebook.select())


if __name__ == '__main__':
    app = Window()
    app.mainloop()