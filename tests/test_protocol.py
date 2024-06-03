import unittest
import socket
import ssl
import threading
import time

from server import main as server_main
from client import main as client_main

class TestChatProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a separate thread
        cls.server_thread = threading.Thread(target=server_main)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        # Add a small delay to ensure the server is up before running tests
        time.sleep(1)

    def setUp(self):
        # Set up a client socket with SSL encryption for each test
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = ssl.wrap_socket(self.client_socket)
        self.client_socket.connect(('127.0.0.1', 12345))

    def tearDown(self):
        # Close the client socket after each test
        self.client_socket.close()

    def test_version_negotiation(self):
        # Test version negotiation between client and server
        version_message = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(version_message, "VERSION 1.0")

        self.client_socket.send(b"VERSION 1.0")
        response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "VERSION OK")

    def test_authentication(self):
        # Test user authentication with the server
        self.client_socket.recv(1024)  # Version message
        self.client_socket.send(b"VERSION 1.0")
        self.client_socket.recv(1024)  # Version OK

        self.client_socket.send(b"user")
        self.client_socket.send(b"pass")
        auth_response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(auth_response, "Enter username:")

    def test_message_exchange(self):
        # Test message exchange between client and server
        self.client_socket.recv(1024)  # Version message
        self.client_socket.send(b"VERSION 1.0")
        self.client_socket.recv(1024)  # Version OK

        self.client_socket.send(b"user")
        self.client_socket.send(b"pass")
        self.client_socket.recv(1024)  # Auth OK

        self.client_socket.send(b"Hello, Anthonio's server!")
        response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "Enter password:")

if __name__ == "__main__":
    unittest.main()
