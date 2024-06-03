import unittest
import socket
import ssl
import sys

sys.path.append('/Users/anthoniomaduadichie/Documents/MSCS/CS 544/Project /Proj_Implementation2')
from server import handle_client

class TestServer(unittest.TestCase):
    def setUp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = ssl.wrap_socket(self.client_socket)
        self.client_socket.connect(('127.0.0.1', 12345))
        self.config = {
            'auth': {
                'username': 'user',
                'password': 'pass'
            }
        }

    def tearDown(self):
        self.client_socket.close()

    def test_version_negotiation(self):
        # Test successful version negotiation
        self.client_socket.send(b"VERSION 1.0")
        handle_client(self.client_socket, None, self.config)
        response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "VERSION OK")

        # Test failed version negotiation
        self.client_socket.send(b"VERSION 0.9")
        handle_client(self.client_socket, None, self.config)
        response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "VERSION MISMATCH")

    def test_authentication(self):
        # Test successful authentication
        self.client_socket.send(b"VERSION 1.0")
        self.client_socket.recv(1024)  # Expect VERSION OK
        self.client_socket.send(b"AUTH|user|pass")
        handle_client(self.client_socket, None, self.config)
        response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "AUTH OK")

        # Test failed authentication
        self.client_socket.send(b"VERSION 1.0")
        self.client_socket.recv(1024)  # Expect VERSION OK
        self.client_socket.send(b"AUTH|user|wrongpass")
        handle_client(self.client_socket, None, self.config)
        response = self.client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "AUTH FAILED")

if __name__ == '__main__':
    unittest.main()
