import socket
import ssl
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description='Client for Chat Protocol over QUIC')
    parser.add_argument('--server-ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=int, default=12345, help='Port to connect to')
    parser.add_argument('--username', type=str, required=True, help='Username for authentication')
    parser.add_argument('--password', type=str, required=True, help='Password for authentication')
    args = parser.parse_args()

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket = ssl.wrap_socket(client_socket)
        client_socket.connect((args.server_ip, args.port))
        logging.info("Connected to the server.")

        # Perform version negotiation
        version = client_socket.recv(1024).decode('utf-8')
        if version != "VERSION 1.0":
            logging.warning("Server version mismatch.")
            client_socket.send(b"VERSION MISMATCH")
            raise ValueError("Server version mismatch")

        client_socket.send(b"VERSION 1.0")
        response = client_socket.recv(1024).decode('utf-8')
        if response != "VERSION OK":
            logging.warning("Version negotiation failed.")
            raise ValueError("Version negotiation failed")

        # Perform authentication
        username = client_socket.recv(1024).decode('utf-8').strip()
        password = client_socket.recv(1024).decode('utf-8').strip()
        auth_response = client_socket.recv(1024).decode('utf-8')
        if auth_response != "AUTH OK":
            logging.warning("Authentication failed.")
            raise ValueError("Authentication failed")
        logging.info("Authentication successful.")

        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            logging.info(f"Server response: {response}")

    except Exception as e:
        logging.error(f"Error communicating with server: {e}")
    finally:
        client_socket.close()
        logging.info("Disconnected from server.")

if __name__ == "__main__":
    main()
