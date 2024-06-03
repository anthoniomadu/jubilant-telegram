import unittest
from unittest.mock import MagicMock
import sys

sys.path.append('/Users/anthoniomaduadichie/Documents/MSCS/CS 544/Project /Proj_Implementation2')
from chat_client import ChatClient

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = ChatClient('127.0.0.1', 12345)
        self.mock_socket = MagicMock()
        self.client.client_socket = self.mock_socket

    def test_connect(self):
        # Test successful connection
        self.mock_socket.recv.side_effect = [b"VERSION OK"]
        result = self.client.connect()
        self.assertTrue(result)

        # Test failed connection
        self.mock_socket.recv.side_effect = [b"VERSION MISMATCH"]
        result = self.client.connect()
        self.assertFalse(result)

    def test_authenticate(self):
        # Test successful authentication
        self.mock_socket.recv.return_value = b"AUTH OK"
        result = self.client.authenticate('user', 'pass')
        self.assertTrue(result)

        # Test failed authentication
        self.mock_socket.recv.return_value = b"AUTH FAILED"
        result = self.client.authenticate('user', 'wrongpass')
        self.assertFalse(result)

    def test_send_message(self):
        # Test sending a message
        self.client.send_message("Hello, server!")
        self.mock_socket.send.assert_called_with(b"Hello, server!")

if __name__ == '__main__':
    unittest.main()
