import json
import socket
from threading import Thread
import time


class Server:
    def __init__(self, server_address):
        """
        :param server_address: например: ('127.0.0.1', 25000)
        """
        self.address = server_address
        self.sock = socket.socket()
        self.sock.bind(self.address)
        self.connections = {}
        self._main_client = None
        self.messages = []
        self._running = True
        self.sock.listen(32)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread = Thread(target=self._waiting_for_connections)
        thread.daemon = True
        thread.start()
        thread = Thread(target=self._send_to_all)
        thread.daemon = True
        thread.start()

    def _waiting_for_connections(self):
        while self._running:
            try:
                connection, address = self.sock.accept()
                if not self._main_client:
                    self._main_client = address
                self.connections.update({connection: json.loads(connection.recv(1024).decode())['userdata']})
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
                self._send_system_message("client " + str(address) + " has disconnected")
                self.connections.pop(connection)
                self._send_current_connections()
                break
            if data:
                messages = data.decode().split("}{")
                if len(messages) > 1:
                    messages = [messages[0] + "}"] + ["{" + i + "}" for i in messages[1:-1]] + ["{" + messages[-1]]
                for message in messages:
                    self._handle_message(message, connection)

    def _handle_message(self, message, connection):
        json_data = json.loads(message)
        if "userdata" in json_data:
            self.connections[connection] = json_data['userdata']
            self._send_current_connections()
        else:
            self.messages.append(message)

    def _send_to_all(self):
        while self._running:
            time.sleep(0.01)
            if self.messages:
                for message in self.messages[:]:
                    for connection in self.connections.keys():
                        connection.sendall(message.encode())
                    self.messages.remove(message)

    def _send_system_message(self, text):
        self.messages.append(json.dumps(
            {"username": "system", "text": text,
             "color": "blue"}))

    def _send_current_connections(self):
        c_list = [c.getpeername() for c in self.connections.keys() if c.getpeername() != self._main_client]
        self.messages.append(json.dumps(
            {"connections_list": c_list}))
        self.messages.append(json.dumps(
            {"users_data": list(self.connections.values())}))

    def stop(self):
        self._running = False
        for connection in list(self.connections.keys()):
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
        self.sock.close()

    def _encrypt(self):
        pass

    def _decrypt(self):
        pass
