import unittest
from unittest.mock import MagicMock
import ssl
import sys

sys.path.append('/Users/anthoniomaduadichie/Documents/MSCS/CS 544/Project /Proj_Implementation2')
from server import handle_client

class TestServer(unittest.TestCase):
    def setUp(self):
        self.client_socket = MagicMock(spec=ssl.SSLSocket)
        self.config = {
            'auth': {
                'username': 'user',
                'password': 'pass'
            }
        }

    def test_version_negotiation(self):
        # Test successful version negotiation
        self.client_socket.recv.side_effect = [b"VERSION 1.0", b"AUTH|user|pass"]
        handle_client(self.client_socket, None, self.config)
        self.client_socket.send.assert_any_call(b"VERSION OK")

        # Test failed version negotiation
        self.client_socket.recv.side_effect = [b"VERSION 0.9"]
        handle_client(self.client_socket, None, self.config)
        self.client_socket.send.assert_called_with(b"VERSION MISMATCH")

    def test_authentication(self):
        # Test successful authentication
        self.client_socket.recv.side_effect = [b"VERSION 1.0", b"AUTH|user|pass"]
        handle_client(self.client_socket, None, self.config)
        self.client_socket.send.assert_any_call(b"AUTH OK")

        # Test failed authentication
        self.client_socket.recv.side_effect = [b"VERSION 1.0", b"AUTH|user|wrongpass"]
        handle_client(self.client_socket, None, self.config)
        self.client_socket.send.assert_called_with(b"AUTH FAILED")

if __name__ == '__main__':
    unittest.main()
