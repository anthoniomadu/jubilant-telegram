import socket
import ssl
import threading
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket, client_address, config):
    logging.info(f"Connection from {client_address} has been established.")
    
    try:
        # Perform version negotiation
        client_socket.send(b"VERSION 1.0")
        version = client_socket.recv(1024).decode('utf-8')
        if version != "VERSION 1.0":
            logging.warning("Client version mismatch.")
            client_socket.send(b"VERSION MISMATCH")
            return
        
        client_socket.send(b"VERSION OK")
        
        # Perform authentication
        client_socket.send(b"Enter username:")
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        client_socket.send(b"Enter password:")
        password = client_socket.recv(1024).decode('utf-8').strip()
        
        if username != config['auth']['username'] or password != config['auth']['password']:
            logging.warning("Authentication failed.")
            client_socket.send(b"AUTH FAILED")
            return
        
        # Send the welcome message after successful authentication
        client_socket.send(b"Welcome to the server!")
        
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            logging.info(f"Received message from {client_address}: {message.decode('utf-8')}")
            client_socket.send(b"Message received")
    
    except ConnectionResetError:
        logging.warning(f"Connection reset by peer: {client_address}")
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection from {client_address} closed.")



def main():
    with open('config.json') as f:
        config = json.load(f)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config['host'], config['port']))
    server_socket.listen(5)
    logging.info(f"Server listening on port {config['port']}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_socket = ssl.wrap_socket(client_socket, server_side=True, certfile=config['certfile'], keyfile=config['keyfile'])
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, config))
        client_handler.start()

if __name__ == "__main__":
    main()
