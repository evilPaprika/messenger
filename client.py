import socket
import json
import re
from threading import Thread

import time

from server import Server


class Client:
    def __init__(self, adress, received_action):
        """
        :param adress: например: '127.0.0.1:25000'
        :param received_action: функция которая будет вызываться при получении сообщения
        """
        self.server_adress = adress
        self.received_action = received_action
        self.sock = socket.socket()
        thread = Thread(target=self._receive_data)
        thread.daemon = True
        thread.start()

    def _receive_data(self):
        try:
            self.sock.connect(self.server_adress)
            self.received_action("system", "connection successful", "blue")
        except socket.error as e:
            self.received_action("system", "unable to connect", "blue")
            print("clent error: " + str(e))
            return
        while True:
            try:
                data = self.sock.recv(1024)
            except socket.error:
                self.received_action("system", "server has disconnected", "blue")
                self.connections_list.sort(key=lambda tup: str(tup))
                if len(self.connections_list) == 0 or self.connections_list[0] == self.sock.getsockname():
                    self.server_adress = ('127.0.0.1', 25000)
                    Server(self.server_adress)
                    self.received_action("system", "you are now hosting server", "blue")
                else:
                    self.server_adress = (self.connections_list[0][0], 25000)
                    time.sleep(1)

                self.sock.close()
                self.sock = socket.socket()
                thread = Thread(target=self._receive_data)
                thread.daemon = True
                thread.start()
                break

            if data:
                self.handle_data(data)

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
                self.received_action(json_data["nickname"], json_data["text"], json_data["color"])

    def send_message(self, name, text):
        self.sock.sendall(json.dumps({"nickname": name, "text": text, "color": "green"}).encode())
