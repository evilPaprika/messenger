import tkinter as tk
from threading import Thread
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


        self.text_input = tk.Text(self, height=5)
        self.text_input.grid(row=1, column=0, columnspan=2, sticky='NSEW')

        btn = Button(self, text="Send", command=self._send_action)
        btn.grid(row=1, column=0, columnspan=2, sticky="NSE")
        self.text_input.bind('<Return>', lambda x: self._send_action())

        if mode == "host":
            self.server = Server(adress)
            self.client = Client(("127.0.0.1", 25000), self.chat_frame.display_message, self.start_new_server)
        elif mode == "connect":
            self.server = None
            self.client = Client(adress, self.chat_frame.display_message, self.start_new_server)
        print(self.client)
        self.side_panel = SidePanelFrame(self.client, self, width=50)
        self.side_panel.grid(row=0, column=1, sticky='NSEW')

    def _send_action(self):
        message_text = self.text_input.get("1.0", 'end-1c')
        self.text_input.delete("1.0", tk.END)  # отчистка поля ввода
        if not message_text: return 'break'
        self.config.read("config.ini")
        self.client.send_message(self.config["USER INFORMATION"]["username"], message_text)
        return 'break'  # preventing Tkinter from propagating event to other handlers.

    def close(self):
        self.side_panel.stop()
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

    def display_message(self, nickname, message_text, color="green"):
        self.configure(state="normal")
        self.insert(tk.END, nickname + ": ", color)
        self.insert(tk.END, message_text + "\n")
        self.configure(state="disabled")


class SidePanelFrame(Frame):
    def __init__(self, client, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self._running = True
        self.client = client
        self.labels = []
        thread = Thread(target=self.update)
        thread.daemon = True
        thread.start()

    def update(self):
        while self._running:
            time.sleep(1)
            if not self.client.has_new_connections_info:
                continue
            self.client.has_new_connections_info = False
            for widget in self.winfo_children():
                widget.destroy()
            self.label = Label(self, text="users:")
            self.label.pack(pady=5)
            for user in self.client.connections_info:
                lbl = Label(self, text=(user["username"] + " :  " + user["status"]), font='Helvetica 10 bold')
                lbl.pack(pady=2)
                self.labels.append(lbl)

    def stop(self):
        self._running = False
