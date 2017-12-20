import json
import socket
import ssl
from threading import Thread
import time


class Server:
    def __init__(self, server_address):
        """
        :param server_address: например: '127.0.0.1:25000'
        """
        self.address = server_address
        self.sock = socket.socket()
        self.sock.bind(self.address)
        self.connections = []
        self.messages = []
        self._running = True
        self.sock.listen(32)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread = Thread(target=self.waiting_for_connections)
        thread.daemon = True
        thread.start()
        thread = Thread(target=self._send_to_all)
        thread.daemon = True
        thread.start()

    def waiting_for_connections(self):
        while self._running:
            try:
                connection, addres = self.sock.accept()
                self.connections.append(connection)
                self._send_connection_list()
                self._send_system_message("new connection established with " + str(addres))
                thread = Thread(target=self.receive_data, args=[connection, addres])
                thread.daemon = True
                thread.start()
            except socket.error as e:
                if not self._running:
                    return
                print("error: seems like you are not connected to the internet")
                print(e)

    def receive_data(self, connection, addres):
        while self._running:
            try:
                data = connection.recv(1024)
            except socket.error:
                self._send_system_message("client " + str(addres) + " has disconected")
                self.connections.remove(connection)
                break
            if data:
                self.messages.append(data.decode())

    def _send_to_all(self):
        while self._running:
            time.sleep(0.01)
            if self.messages:
                for message in self.messages[:]:
                    for connection in self.connections:
                        connection.sendall(message.encode())
                    self.messages.remove(message)

    def _send_system_message(self, text):
        self.messages.append(json.dumps(
            {"nickname": "system", "text": text,
             "color": "blue"}))

    def _send_connection_list(self):
        c_list = [c.getpeername() for c in self.connections][1:]
        self.messages.append(json.dumps(
            {"connections_list": c_list}))

    def stop(self):
        self._running = False
        time.sleep(0.2)
        for connection in self.connections:
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
        self.sock.close()

    def encrypt(self):
        pass
