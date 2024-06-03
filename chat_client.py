import socket
import ssl
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatClient:
    def __init__(self, server_ip, port, username, password):
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.password = password
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket = ssl.wrap_socket(self.client_socket)
            self.client_socket.connect((self.server_ip, self.port))
            logging.info("Connected to the server.")
            return True
        except Exception as e:
            logging.error(f"Error connecting to server: {e}")
            return False

    def authenticate(self):
        try:
            # Send authentication information in a specific format
            auth_message = f"AUTH|{self.username}|{self.password}"
            self.client_socket.send(auth_message.encode('utf-8'))
            auth_response = self.client_socket.recv(1024).decode('utf-8')
            if auth_response == "AUTH OK":
                logging.info("Authentication successful.")
                return True
            else:
                logging.warning("Authentication failed.")
                return False
        except Exception as e:
            logging.error(f"Error authenticating: {e}")
            return False


    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            logging.info(f"Server response: {response}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def disconnect(self):
        try:
            if self.client_socket:
                self.client_socket.close()
                logging.info("Disconnected from server.")
        except Exception as e:
            logging.error(f"Error disconnecting from server: {e}")

def main():
    parser = argparse.ArgumentParser(description='Client for Chat Protocol over QUIC')
    parser.add_argument('--server-ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=int, default=12345, help='Port to connect to')
    parser.add_argument('--username', type=str, required=True, help='Username for authentication')
    parser.add_argument('--password', type=str, required=True, help='Password for authentication')
    args = parser.parse_args()

    client = ChatClient(args.server_ip, args.port, args.username, args.password)
    if client.connect() and client.authenticate():
        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                break
            client.send_message(message)
        client.disconnect()

if __name__ == "__main__":
    main()
