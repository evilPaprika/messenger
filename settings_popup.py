import tkinter as tk
from tkinter.ttk import *
import socket
import configparser


# Всплывающее окно с настройками
# Ввод сохраняется в config.ini
class Settings(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("settings")
        self.geometry("250x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        Label(self, text="your IP: " + socket.gethostbyname(socket.gethostname())).grid(columnspan=2, pady=(15, 25))
        Label(self, text="username: ").grid(row=1, sticky='E')
        Label(self, text="color: ").grid(row=2, sticky='E')

        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.username_entry = Entry(self)
        self.username_entry.grid(row=1, column=1, sticky='W')
        self.color_entry = Entry(self)
        self.color_entry.grid(row=2, column=1, sticky='W')
        try:
            self.username_entry.insert(0, self.config["USER INFORMATION"]["username"])
            self.color_entry.insert(0, self.config["USER INFORMATION"]["color"])
        except:
            pass

        Button(self, text="apply", width=20, command=self.save_input).grid(row=3, column=0, columnspan=2, pady=30)

    def save_input(self):
        self.config.set("USER INFORMATION",  "username", self.username_entry.get())
        self.config.set("USER INFORMATION",  "color", self.color_entry.get())

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        self.destroy()
