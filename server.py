import json
import socket
from threading import Thread
import time


class Server:
    def __init__(self, server_address):
        """
        :param server_address: например: '127.0.0.1:25000'
        """
        self.adress = server_address
        self.sock = socket.socket()
        self.sock.bind(self.adress)
        self.connections = []
        self.messages = []
        self.sock.listen(32)
        thread = Thread(target=self.waiting_for_connections)
        thread.daemon = True
        thread.start()
        thread = Thread(target=self._send_to_all)
        thread.daemon = True
        thread.start()

    def waiting_for_connections(self):
        while True:
            connection, addres = self.sock.accept()
            self.connections.append(connection)
            self._send_connection_list()
            self._send_system_message("new connection established with " + str(addres))
            thread = Thread(target=self.receive_data, args=[connection, addres])
            thread.daemon = True
            thread.start()

    def receive_data(self, connection, addres):
        while True:
            try:
                data = connection.recv(1024)
            except:
                self._send_system_message("client " + str(addres) + " has disconected")
                self.connections.remove(connection)
                break
            if data:
                self.messages.append(data)

    def _send_to_all(self):
        while True:
            time.sleep(0.01)
            if self.messages:
                for message in self.messages[:]:
                    for connection in self.connections:
                        connection.sendall(message)
                    self.messages.remove(message)

    def _send_system_message(self, text):
        self.messages.append(json.dumps(
            {"nickname": "system", "text": text,
             "color": "blue"}).encode())

    def _send_connection_list(self):
        c_list = [c.getpeername() for c in self.connections][1:]
        self.messages.append(json.dumps(
            {"connections_list": c_list}).encode())
