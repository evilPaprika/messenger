import tkinter as tk
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from client import Client
from server import Server
import configparser


class Chat(Frame):
    def __init__(self, parent, mode, adress):
        Frame.__init__(self, parent)
        self.parent = parent
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.chat_frame = ChatFrame(self)
        self.chat_frame.grid(row=0, column=0, sticky='NSEW')

        self.text_input = tk.Text(self, height=5)
        self.text_input.grid(row=1, column=0, columnspan=2, sticky='NSEW')

        btn = Button(self, text="Send", command=self.send_action)
        btn.grid(row=1, column=0, columnspan=2, sticky="NSE")

        if mode == "host":
            Server(adress)
            self.client = Client(adress, self.chat_frame.add_message)
        else:
            self.client = Client(adress, self.chat_frame.add_message)


    def send_action(self):
        message_text = self.text_input.get("1.0", 'end-1c')
        if not message_text: return
        self.text_input.delete("1.0", tk.END) # отчистка поля ввода

        self.config.read("config.ini")
        self.client.send_data(self.config["USER INFORMATION"]["username"], message_text)


class ChatFrame(ScrolledText):
    def __init__(self, *args, **kwargs):
        ScrolledText.__init__(self, *args, **kwargs)
        self.config(bg="#e6ebf4")
        self.pack(expand=1, fill="both")
        self.bind("<1>", lambda event: self.focus_set()) # разрешить копирование
        self.configure(state="disabled")

        for color in ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink']:
            self.tag_configure(color, foreground=color, font=("Courier", "11", "bold"))


    def add_message(self, nickname, message_text, color="green"):
        self.configure(state="normal")
        self.insert(tk.END, nickname + ": ", color)
        self.insert(tk.END, message_text + "\n")
        self.configure(state="disabled")
