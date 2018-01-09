import configparser
import socket
import json
from threading import Thread
import time
import os
from encryption import Encryption


class Client:
    def __init__(self, address, display_message, start_new_server):
        """
        :param address: адресс сервера, например: ('127.0.0.1' , 25000)
        :param display_message: функция которая будет вызываться при получении сообщения
        :param start_new_server: функция которая будет вызываться когда нужно создать новый сервер
        """
        self.server_address = address
        self.display_message = display_message
        self._start_new_server = start_new_server
        self.connections_list = []
        self.connections_info = []
        self._encryption = Encryption()
        self.has_new_connections_info = True
        self._running = True
        self.sock = socket.socket()
        thread = Thread(target=self._receive_data)
        thread.daemon = True
        thread.start()

    def _receive_data(self):
        try:
            self.sock.connect(self.server_address)
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
                    self._handle_data(data)
            except socket.error:
                if not self._running:
                    return
                self.display_message("system", "server has disconnected", "blue")
                self._handle_server_down()
                break

    def _handle_data(self, data):
        # данные в посылаются в формате json
        messages = self._encryption.decrypt(data).decode().split("}{") # разделение пакетов json
        if len(messages) > 1:
            messages = [messages[0] + "}"] + ["{" + i + "}" for i in messages[1:-1]] + ["{" + messages[-1]]
        for message in messages:
            self._handle_message(message)

    def send_message(self, name, text, color):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.sock.sendall(self._encryption.encrypt(json.dumps({"username":  name,
                                      "text": text, "color": color}).encode()))

    def _handle_message(self, message):
        json_data = json.loads(message)
        if "connections_list" in json_data:
            if len(json_data["connections_list"]) == 0:
                self.connections_list = []
            else:
                self.connections_list = [tuple(l) for l in json_data["connections_list"]]
        elif "users_data" in json_data:
            self.connections_info = list(json_data["users_data"])
            self.has_new_connections_info = True
        else:
            self.display_message(json_data["username"], json_data["text"], json_data["color"])

    def _handle_server_down(self):
        # обработка отключения сервера, выбор клиента создающеко новый сервер
        self.connections_list.sort(key=lambda tup: str(tup))
        if self.connections_list[0] == self.sock.getsockname():
            self._start_new_server(('', 25000))
            self.server_address = ('127.0.0.1', 25000)
            self.display_message("system", "you are now hosting server", "blue")
        else:
            self.server_address = (self.connections_list[0][0], 25000)
            time.sleep(1)

        self.sock.close()
        self.sock = socket.socket()
        thread = Thread(target=self._receive_data)
        thread.daemon = True
        thread.start()

    def _send_description(self):
        # отправляет описание пользователя, когда требуется
        prev_modified = 0
        while self._running:
            modified = os.path.getmtime("config.ini")
            if prev_modified < modified:
                config = configparser.ConfigParser()
                config.read("config.ini")
                name = config.get("USER INFORMATION", "username")
                color = config.get("USER INFORMATION", "color")
                status = config.get("USER INFORMATION", "status")
                self.sock.sendall(self._encryption.encrypt(
                    json.dumps({"userdata": {"username": name, "color": color, "status": status}}).encode()))
                prev_modified = modified
            time.sleep(1)

    def stop(self):
        self._running = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
