import socket
import ssl
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')


class ChatClient:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket = ssl.wrap_socket(self.client_socket)
            self.client_socket.connect((self.server_ip, self.port))
            logging.info("Connected to the server.")

            # Perform version negotiation
            version = self.client_socket.recv(1024).decode('utf-8')
            if version != "VERSION 1.0":
                logging.warning("Server version mismatch.")
                return False

            self.client_socket.send(b"VERSION 1.0")
            response = self.client_socket.recv(1024).decode('utf-8')
            if response != "VERSION OK":
                logging.warning("Version negotiation failed.")
                return False

            logging.info("Version negotiation successful.")
            return True
        except Exception as e:
            logging.error(f"Error connecting to server: {e}")
            return False

    def authenticate(self, username, password):
        try:
            # Send authentication information in a specific format
            auth_message = f"AUTH|{username}|{password}"
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
    print("============================================================================")
    print("Welcome to the Jubilant Telegram Chat Protocol over QUIC Client Application!")
    print("============================================================================")
    print("Description: This client application allows you to connect to the jubilant telegram chat server and exchange messages securely using the QUIC protocol.")
    print()

    parser = argparse.ArgumentParser(description='Client for Chat Protocol over QUIC')
    parser.add_argument('--server-ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=int, default=12345, help='Port to connect to')
    args = parser.parse_args()

    client = ChatClient(args.server_ip, args.port)

    if client.connect():
        username = input("Enter username: ")
        password = input("Enter password: ")

        if client.authenticate(username, password):
            print("Authentication successful. Now you can now send messages in a jubilant way.")
            print("---------------------------------------------------------------------------")

            while True:
                message = input("Enter message (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                client.send_message(message)

        else:
            print("Authentication failed. Exiting...")

        client.disconnect()
    else:
        print("Failed to connect to the server. Exiting...")


if __name__ == "__main__":
    main()