import json
import socket
from threading import Thread


class Server:
    def __init__(self, adress):
        """
        :param adress: например: '127.0.0.1:25000'
        :param received_action: функция которая будет вызываться при получении сообщения
        """

        self.adress =  adress
        self.sock = socket.socket()
        self.sock.bind(self.adress)
        self.connections = []
        self.messages = []
        self.sock.listen(32)
        thread = Thread(target=self.waiting_for_connections)
        thread.daemon = True
        thread.start()
        thread = Thread(target=self.send_data)
        thread.daemon = True
        thread.start()


    def waiting_for_connections(self):
        while True:
            connection, addres = self.sock.accept()
            self.connections.append(connection)
            self._send_system_message("new connection established with " + str(addres))
            thread = Thread(target=self.receive_data, args=[connection, addres])
            thread.daemon = True
            thread.start()

    def receive_data(self, connection, addres):
        while True:
            try:
                data = connection.recv(1024)
            except:
                self._send_system_message("client "  + str(addres) + " has disconected")
                break

            if data:
                self.messages.append(data)



    def send_data(self):
        while True:
            if self.messages:
                for message in self.messages[:]:
                    for connection in self.connections:
                        connection.sendall(message)
                    self.messages.remove(message)

    def _send_system_message(self, text):
        self.messages.append(json.dumps(
            {"nickname": "system", "text": text,
             "color": "blue"}).encode())
