# Chat Protocol over QUIC

## Overview

This project implements a chat protocol over QUIC using Python. It includes state management, message transmission, error handling, version negotiation, and authentication.

## Prerequisites

- Python 3.x
- Required libraries: `argparse`, `socket`, `ssl`, `threading`, `logging`

## Installation

1. Clone the repository.
2. Install dependencies:
3. Ensure you have the server certificate (`server.crt`) and key (`server.key`) in the project directory.

## Configuration

Modify the `config.json` file to set the server configuration:

{
"host": "127.0.0.1",
"port": 12345,
"certfile": "server.crt",
"keyfile": "server.key",
"auth": {
"username": "user",
"password": "pass"
}
}


## Usage

### To run the server: Open a terminal window.

1. Start the server:

Run the server script using the command python3 server.py --config config.json.

#### Keep this terminal window open to keep the server running.

###To run the client: Open another terminal window. Navigate to the directory containing the client.py script.


2. Start the client: Run the client script using the command

python3 chat_client.py --server-ip 127.0.0.1 --port 12345


The client will connect to the server using the provided server IP address, port number, username, and password.
## Enter User name: user
## Enter Password: pass

## Tests

Unit and integration tests are located in the `tests/` directory.

To run the tests:

python3 -m unittest discover -s tests


## Certificate Generation

To generate a self-signed certificate and key, you can use OpenSSL:

openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes


## Project Structure

- `server.py`: The server implementation.
- `client.py`: The client implementation.
- `config.json`: Configuration file for server settings.
- `README.md`: Instructions on how to compile and run the application.
- `requirements.txt`: Required Python libraries.
- `tests/`: Directory for unit and integration tests.

## Conclusion

This implementation provides a robust chat protocol over QUIC with state management, message transmission, error handling, version negotiation, and authentication. 
The server can handle multiple clients using threading, and the communication is secured with TLS. The project is well-documented, includes automated testing, and uses a cloud-based Git system for version control and community engagement.
