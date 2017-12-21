import tkinter as tk
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import time
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


        self.chat_frame = MessagesFrame(self)
        self.chat_frame.grid(row=0, column=0, sticky='NSEW')

        self.columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, minsize=150)
        self.side_panel = SidePanelFrame(self, width=50)
        self.side_panel.grid(row=0, column=1, sticky='NSEW')

        self.text_input = tk.Text(self, height=5)
        self.text_input.grid(row=1, column=0, columnspan=2, sticky='NSEW')

        btn = Button(self, text="Send", command=self.send_action)
        btn.grid(row=1, column=0, columnspan=2, sticky="NSE")
        self.text_input.bind('<Return>', lambda x: self.send_action())

        if mode == "host":
            self.server = Server(adress)
            self.client = Client(("127.0.0.1",25000), self.chat_frame.add_message, self.start_new_server)
        elif mode == "connect":
            self.server = None
            self.client = Client(adress, self.chat_frame.add_message, self.start_new_server)

    def send_action(self):
        message_text = self.text_input.get("1.0", 'end-1c')
        self.text_input.delete("1.0", tk.END)  # отчистка поля ввода
        if not message_text: return 'break'
        self.config.read("config.ini")
        self.client.send_message(self.config["USER INFORMATION"]["username"], message_text)
        return 'break'  # preventing Tkinter from propagating event to other handlers.

    def close(self):
        self.client.stop()
        time.sleep(0.1)
        if self.server:
            self.server.stop()

    def start_new_server(self, address):
        self.server = Server(address)


class MessagesFrame(ScrolledText):
    def __init__(self, *args, **kwargs):
        ScrolledText.__init__(self, *args, **kwargs)
        self.config(bg="#e6ebf4")
        self.pack(expand=1, fill="both")
        self.bind("<1>", lambda event: self.focus_set())  # разрешить копирование
        self.configure(state="disabled")

        for color in ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink']:
            self.tag_configure(color, foreground=color, font=("Courier", "11", "bold"))

    def add_message(self, nickname, message_text, color="green"):
        self.configure(state="normal")
        self.insert(tk.END, nickname + ": ", color)
        self.insert(tk.END, message_text + "\n")
        self.configure(state="disabled")


class SidePanelFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self._running = True
        self.label = Label(self, text="users:")
        self.label1 = Label(self, text="1")
        self.label2 = Label(self, text="2")
        self.label3 = Label(self, text="3")

        self.label.pack()
        self.label1.pack()
        self.label2.pack()
        self.label3.pack()
        self.label1.configure(text="")

    def update(self):
        pass

    def stop(self):
        self._running = False
