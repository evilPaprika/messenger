import configparser
from tkinter import *
from tkinter import ttk

import gc

import menu_frame
import settings_popup
from chat_frame import Chat


class Window(Tk):
    """   главное окно GUI   """

    def __init__(self):
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

        cascade = Menu(self)
        menubar.add_cascade(label="status", menu=cascade)
        cascade.add_command(label="available", command=lambda: self.set_status("available"))
        cascade.add_command(label="away", command=lambda: self.set_status("away"))
        cascade.add_command(label="do not disturb", command=lambda: self.set_status("do not disturb"))

        self.config(menu=menubar)
        self.create_new_tab()

    def create_new_tab(self):
        frame = menu_frame.Menu(self)
        self.notebook.add(frame, text="new tab")
        self.notebook.select(len(self.notebook.tabs()) - 1)

    def close_current_tab(self):
        if len(self.notebook.tabs()) == 0: return
        tab_index = self.notebook.index(self.notebook.select())
        if tab_index in self.frames:
            self.frames[tab_index].close()
            self.frames.pop(tab_index)
        self.notebook.forget(self.notebook.select())

    def update_tab(self, frame, new_text):
        tab_index = self.notebook.index(self.notebook.select())
        if isinstance(frame, Chat):
            self.frames[tab_index] = frame
        self.notebook.forget(self.notebook.select())
        if tab_index != len(self.notebook.tabs()):        # нельзя сделать инсерт в конец вкладок
            self.notebook.insert(tab_index, frame, text=new_text)
        else:
            self.notebook.add(frame, text=new_text)
            self.notebook.select(tab_index)

    def set_status(self, status):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set("USER INFORMATION", "status", status)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

if __name__ == '__main__':
    app = Window()
    app.mainloop()
