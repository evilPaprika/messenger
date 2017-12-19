import tkinter as tk
from tkinter.ttk import *
import chat_frame

class Menu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)


        # интерфейс подсоеденения
        Label(self, text="connect to existing chat:", font=("Helvetica", 14)).grid(pady=15, columnspan=2)
        # Label(self, text="enter adress (ip:port):").grid(row=1, column=0, sticky="E")
        Label(self, text="enter ip adress:").grid(row=1, column=0, sticky="E")
        self.connect_entry = tk.Entry(self)
        # self.connect_entry.insert(tk.END, '127.0.0.1:25000')
        self.connect_entry.insert(tk.END, '127.0.0.1')
        self.connect_entry.grid(row=1, column=1, sticky='W')
        Button(self, text="connect", command=self.connect_action, width=25).grid(row=3, column=0, padx=50, pady=20,
                                                                               columnspan=2)

        # интерфейс создания нового чата
        Label(self, text="create new chat: ", font=("Helvetica", 14)).grid(row=0, column=2, pady=15, columnspan=2)
        # Label(self, text="enter port:").grid(row=1, column=2, sticky='E')
        # self.host_entry = tk.Entry(self)
        # self.host_entry.insert(tk.END, '25000')
        # self.host_entry.grid(row=1, column=3, sticky='W')
        Button(self, text="create", command=self.host_action, width=25).grid(row=3, column=2, padx=50, pady=20,
                                                                              columnspan=2)


    def connect_action(self):
        addres = (self.connect_entry.get(), 25000)
        # try:
        #     addres = self.connect_entry.get().split(":")
        #     addres = (addres[0], int(addres[1]))
        # except:
        #     self.connect_entry.config(background="pink")
        #     return
        tab_index = self.parent.index(self.parent.select())
        self.parent.forget(self.parent.select())

        if tab_index != len(self.parent.tabs()):        # нельзя сделать инсерт в конец вкладок
            self.parent.insert(tab_index, chat_frame.Chat(self.parent, "connect", addres),
                               text=self.connect_entry.get())
        else:
            self.parent.add(chat_frame.Chat(self.parent, "connect", addres), text=self.connect_entry.get())

        self.parent.select(tab_index)


    def host_action(self):
        addres = ("", 25000)
        # try:
        #     addres = ("127.0.0.1", int(self.host_entry.get()))
        # except:
        #     self.host_entry.config(background="pink")
        #     return
        tab_index = self.parent.index(self.parent.select())
        self.parent.forget(self.parent.select())

        if tab_index != len(self.parent.tabs()):        # нельзя сделать инсерт в конец вкладок
            self.parent.insert(tab_index,
                               chat_frame.Chat(self.parent, "host",  addres), text='{}:{}'.format(addres[0], addres[1]))
        else:
            self.parent.add(chat_frame.Chat(self.parent, "host", addres), text='{}:{}'.format(addres[0], addres[1]))

        self.parent.select(tab_index)

