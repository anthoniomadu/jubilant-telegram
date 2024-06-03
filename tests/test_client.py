import unittest
from unittest.mock import patch, MagicMock
import socket
import ssl
import sys

sys.path.append('/Users/anthoniomaduadichie/Documents/MSCS/CS 544/Project /Proj_Implementation2')
from chat_client import ChatClient

class TestChatClient(unittest.TestCase):
    def setUp(self):
        self.client = ChatClient('127.0.0.1', 12345)
        self.mock_socket = MagicMock()
        self.client.client_socket = self.mock_socket

    @patch('socket.socket')
    @patch('ssl.wrap_socket')
    def test_connect(self, mock_wrap_socket, mock_socket):
        mock_ssl_socket_instance = mock_wrap_socket.return_value

        # Test successful connection and version negotiation
        mock_ssl_socket_instance.recv.side_effect = [b"VERSION 1.0", b"VERSION OK"]
        result = self.client.connect()
        self.assertTrue(result)
        mock_ssl_socket_instance.send.assert_called_with(b"VERSION 1.0")

        # Test server version mismatch
        mock_ssl_socket_instance.recv.side_effect = [b"VERSION 0.9"]
        result = self.client.connect()
        self.assertFalse(result)

        # Test version negotiation failure
        mock_ssl_socket_instance.recv.side_effect = [b"VERSION 1.0", b"VERSION MISMATCH"]
        result = self.client.connect()
        self.assertFalse(result)

    @patch('socket.socket')
    @patch('ssl.wrap_socket')
    def test_authenticate(self, mock_wrap_socket, mock_socket):
        # Mocking the socket and wrap_socket functions
        mock_wrap_socket.return_value = self.mock_socket
        mock_socket.return_value = self.mock_socket

        # Test successful authentication
        self.mock_socket.recv.side_effect = [b"AUTH OK"]
        result = self.client.authenticate('user', 'pass')
        self.assertTrue(result)

        # Test failed authentication
        self.mock_socket.recv.side_effect = [b"AUTH FAILED"]
        result = self.client.authenticate('user', 'wrongpass')
        self.assertFalse(result)
        
    def test_send_message(self):
        self.client.send_message("Hello, server!")
        self.mock_socket.send.assert_called_with(b"Hello, server!")

    def test_disconnect(self):
        self.client.disconnect()
        self.mock_socket.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
