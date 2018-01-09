import unittest
import time
from client import Client
from server import Server


class TestMessenger(unittest.TestCase):
    def set_to_default(self):
        self.received_message = ""
        self.received_message = ""
        self.received_message = ""

    def receive(self, name, text, color):
        self.received_name = name
        self.received_message = text
        self.received_color = color

    def test_send_message_to_self(self):
        self.set_to_default()
        server = Server(('127.0.0.1', 25000))
        client = Client(('127.0.0.1', 25000), self.receive, None)
        time.sleep(0.2)
        client.send_message("test", "Hello", "red")
        time.sleep(0.2)
        self.assertEqual("Hello", self.received_message)
        self.assertEqual("test", self.received_name)
        self.assertEqual("red", self.received_color)
        client.stop()
        time.sleep(0.2)
        server.stop()

    def test_send_message_to_another(self):
        self.set_to_default()
        server = Server(('127.0.0.1', 25000))
        client1 = Client(('127.0.0.1', 25000), lambda x, y, z: None, None)
        client2 = Client(('127.0.0.1', 25000), self.receive, None)
        time.sleep(0.2)
        client1.send_message("test", "Hello", "red")
        time.sleep(0.2)
        self.assertEqual("Hello", self.received_message)
        self.assertEqual("test", self.received_name)
        self.assertEqual("red", self.received_color)
        client1.stop()
        client2.stop()
        time.sleep(0.2)
        server.stop()

    def test_decentralisation(self):
        self.set_to_default()

        def create_new_server(address):
            nonlocal server
            server = Server(address)

        server = Server(('127.0.0.1', 25000))
        client1 = Client(('127.0.0.1', 25000), lambda x, y, z: None, create_new_server)
        client2 = Client(('127.0.0.1', 25000), self.receive, create_new_server)
        time.sleep(1)
        server.stop()
        time.sleep(2)
        client1.send_message("test", "Hello", "red")
        time.sleep(0.2)
        self.assertEqual("Hello", self.received_message)
        self.assertEqual("test", self.received_name)
        self.assertEqual("red", self.received_color)
        client1.stop()
        client2.stop()
        time.sleep(0.2)
        server.stop()


if __name__ == '__main__':
    unittest.main()
