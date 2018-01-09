import json
import socket
from threading import Thread
import time
from encryption import Encryption


class Server:
    def __init__(self, server_address):
        """
        :param server_address: например: ('127.0.0.1', 25000)
        """
        self.address = server_address
        self._sock = socket.socket()
        self._sock.bind(self.address)
        self._connections = {}
        self._main_client = None
        self._messages = []
        self._encryption = Encryption()
        self._running = True
        self._sock.listen(32)

        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread = Thread(target=self._waiting_for_connections)
        thread.daemon = True
        thread.start()
        thread = Thread(target=self._send_to_all)
        thread.daemon = True
        thread.start()

    def _waiting_for_connections(self):
        while self._running:
            try:
                connection, address = self._sock.accept()
                if not self._main_client:
                    self._main_client = address
                self._connections.update({connection: json.loads(
                    self._encryption.decrypt(connection.recv(1024)).decode())['userdata']})
                self._send_current_connections()
                self._send_system_message("new connection established with " + str(address))
                thread = Thread(target=self.receive_data, args=[connection, address])
                thread.daemon = True
                thread.start()
            except socket.error as e:
                if not self._running:
                    return
                print("error: seems like you are not connected to the internet")
                print(e)

    def receive_data(self, connection, address):
        while self._running:
            try:
                data = connection.recv(1024)
            except socket.error:
                if not self._running:
                    break
                self._send_system_message("client " + str(address) + " has disconnected")
                self._connections.pop(connection)
                self._send_current_connections()
                break
            if data:
                messages = self._encryption.decrypt(data).decode().split("}{")
                if len(messages) > 1:
                    messages = [messages[0] + "}"] + ["{" + i + "}" for i in messages[1:-1]] + ["{" + messages[-1]]
                for message in messages:
                    self._handle_message(message, connection)

    def _handle_message(self, message, connection):
        json_data = json.loads(message)
        if "userdata" in json_data:
            self._connections[connection] = json_data['userdata']
            self._send_current_connections()
        else:
            self._messages.append(message)

    def _send_to_all(self):
        while self._running:
            if self._messages:
                for message in self._messages[:]:
                    for connection in self._connections.keys():
                        connection.sendall(self._encryption.encrypt(message.encode()))
                    self._messages.remove(message)
                    time.sleep(0.1)
            time.sleep(0.01)

    def _send_system_message(self, text):
        self._messages.append(json.dumps(
            {"username": "system", "text": text,
             "color": "blue"}))

    def _send_current_connections(self):
        c_list = [c.getpeername() for c in self._connections.keys() if c.getpeername() != self._main_client]
        self._messages.append(json.dumps(
            {"connections_list": c_list}))
        time.sleep(0.1)
        self._messages.append(json.dumps(
            {"users_data": list(self._connections.values())}))

    def stop(self):
        self._running = False
        for connection in list(self._connections.keys()):
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
        self._sock.close()
