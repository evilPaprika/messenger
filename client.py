import socket
import json
from threading import Thread


class Client:
    def __init__(self, adress, received_action):
        """
        :param adress: например: '127.0.0.1:25000'
        :param received_event: функция которая будет вызываться при получении сообщения
        """
        self.adress = adress
        self.received_action = received_action
        self.sock = socket.socket()
        thread = Thread(target=self.receive_data)
        thread.daemon = True
        thread.start()


    def receive_data(self):
        try:
            self.sock.connect(self.adress)
            self.received_action(*("system", "connection successful", "blue"))
        except Exception as e:
            self.received_action(*("system", "unable to connect", "blue"))
            print(e)
            return

        while True:
            try:
                data = self.sock.recv(1024)
            except:
                self.received_action(*("system", "server has disconnected", "blue"))
                break

            if data:
                json_data = json.loads(data)
                self.received_action(json_data["nickname"], json_data["text"], json_data["color"])



    def send_data(self, name, text):
        self.sock.sendall(json.dumps({"nickname" : name, "text" : text, "color": "green"}).encode())

