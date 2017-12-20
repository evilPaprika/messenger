import tkinter as tk
from tkinter.ttk import *
import chat_frame

class Menu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.notebook)
        self.notebook = parent.notebook
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # интерфейс подсоеденения
        Label(self, text="connect to existing chat:", font=("Helvetica", 14)).grid(pady=15, columnspan=2)
        Label(self, text="enter ip adress:").grid(row=1, column=0, sticky="E")
        self.connect_entry = tk.Entry(self)
        self.connect_entry.insert(tk.END, '127.0.0.1')
        self.connect_entry.grid(row=1, column=1, sticky='W')
        Button(self, text="connect", command=self.connect_action, width=25).grid(row=3, column=0, padx=50, pady=20,
                                                                               columnspan=2)
        # интерфейс создания нового чата
        Label(self, text="create new chat: ", font=("Helvetica", 14)).grid(row=0, column=2, pady=15, columnspan=2)
        Button(self, text="create", command=self.host_action, width=25).grid(row=3, column=2, padx=50, pady=20,
                                                                              columnspan=2)
    def connect_action(self):
        addres = (self.connect_entry.get(), 25000)
        self.parent.update_tab(chat_frame.Chat(self.notebook, "connect", addres), self.connect_entry.get())

    def host_action(self):
        addres = ("", 25000)
        self.parent.update_tab(chat_frame.Chat(self.notebook, "host", addres), '{}:{}'.format(addres[0], addres[1]))



