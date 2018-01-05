import configparser
import socket
import json
import re
import ssl
from threading import Thread

import time

import os

from server import Server


class Client:
    def __init__(self, adress, display_message, start_new_server):
        """
        :param adress: например: '127.0.0.1'
        :param received_action: функция которая будет вызываться при получении сообщения
        :param start_new_server: функция которая будет вызываться когда нужно создать новый сервер
        """
        self.server_adress = adress
        self.display_message = display_message
        self._start_new_server = start_new_server
        self.connections_list = []
        self._running = True
        self.sock = socket.socket()
        thread = Thread(target=self._receive_data)
        thread.daemon = True
        thread.start()

    def _receive_data(self):
        try:
            self.sock.connect(self.server_adress)
            self.display_message("system", "connection successful", "blue")
            thread = Thread(target=self._send_description)
            thread.daemon = True
            thread.start()
        except socket.error as e:
            self.display_message("system", "unable to connect", "blue")
            print("clent error: " + str(e))
            return
        while self._running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    raise socket.error
                else:
                    self.handle_data(data)
            except socket.error as e:
                print(e)
                if not self._running: return
                self.display_message("system", "server has disconnected", "blue")
                self.connections_list.sort(key=lambda tup: str(tup))
                if self.connections_list[0] == self.sock.getsockname():
                    self._start_new_server(('', 25000))
                    self.server_adress = ('127.0.0.1', 25000)
                    self.display_message("system", "you are now hosting server", "blue")
                else:
                    self.server_adress = (self.connections_list[0][0], 25000)
                    time.sleep(1)

                self.sock.close()
                self.sock = socket.socket()
                thread = Thread(target=self._receive_data)
                thread.daemon = True
                thread.start()
                break

    def handle_data(self, data):
        # print(data.decode())
        messages = re.split('({[^}]*})', data.decode())[1::2]
        for message in messages:
            json_data = json.loads(message)
            if "connections_list" in json_data:
                if len(json_data["connections_list"]) == 0:
                    self.connections_list = []
                else:
                    self.connections_list = [tuple(l) for l in json_data["connections_list"]]
            else:
                self.display_message(json_data["nickname"], json_data["text"], json_data["color"])

    def send_message(self, name, text):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.sock.sendall(json.dumps({"nickname":  config.get("USER INFORMATION", "username"), "text": text, "color": config.get("USER INFORMATION", "color")}).encode())

    def _send_description(self):
        prev_modified = 0
        while self._running:
            modified = os.path.getmtime("config.ini")
            if prev_modified < modified:
                print(modified)
                config = configparser.ConfigParser()
                config.read("config.ini")
                name = config.get("USER INFORMATION", "username")
                color = config.get("USER INFORMATION", "color")
                status = config.get("USER INFORMATION", "status")
                self.sock.sendall(json.dumps({"userdata": {"username": name, "color": color, "status": status}}).encode())
                prev_modified = modified
            time.sleep(1)

    def stop(self):
        self._running = False
        self.sock.close()
