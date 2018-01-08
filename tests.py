import unittest
import time
from client import Client
from server import Server


class TestMessenger(unittest.TestCase):
    def test_send_message_to_self(self):
        received_message = ""
        received_name = ""
        received_color = ""
        def receive(name, text, color):
            nonlocal received_message
            nonlocal received_name
            nonlocal received_color
            received_name = name
            received_message = text
            received_color = color
        server = Server(('127.0.0.1', 25000))
        client = Client(('127.0.0.1', 25000), receive, None)
        time.sleep(0.2)
        client.send_message("test", "Hello", "red")
        time.sleep(0.2)
        self.assertEqual("Hello", received_message)
        self.assertEqual("test", received_name)
        self.assertEqual("red", received_color)
        client.stop()
        time.sleep(0.1)
        server.stop()
        time.sleep(0.2)

    def test_send_message_to_another(self):
        received_message = ""
        received_name = ""
        received_color = ""
        def receive(name, text, color):
            nonlocal received_message
            nonlocal received_name
            nonlocal received_color
            received_name = name
            received_message = text
            received_color = color
        server = Server(('127.0.0.1', 25000))
        client1 = Client(('127.0.0.1', 25000), lambda x, y, z: None, None)
        client2 = Client(('127.0.0.1', 25000), receive, None)
        time.sleep(0.2)
        client1.send_message("test", "Hello", "red")
        time.sleep(0.2)
        self.assertEqual("Hello", received_message)
        self.assertEqual("test", received_name)
        self.assertEqual("red", received_color)
        client1.stop()
        client2.stop()
        time.sleep(0.1)
        server.stop()

    def test_decentralisation(self):
        received_message = ""
        received_name = ""
        received_color = ""
        def receive(name, text, color):
            nonlocal received_message
            nonlocal received_name
            nonlocal received_color
            received_name = name
            received_message = text
            received_color = color
        def create_new_server(address):
            nonlocal server
            server = Server(address)
        server = Server(('127.0.0.1', 25000))
        client1 = Client(('127.0.0.1', 25000), lambda x, y, z: None, create_new_server)
        client2 = Client(('127.0.0.1', 25000), receive, create_new_server)
        time.sleep(1)
        server.stop()
        time.sleep(2)
        client1.send_message("test", "Hello", "red")
        time.sleep(0.2)
        self.assertEqual("Hello", received_message)
        self.assertEqual("test", received_name)
        self.assertEqual("red", received_color)
        client1.stop()
        client2.stop()
        time.sleep(0.1)
        server.stop()


if __name__ == '__main__':
    unittest.main()
