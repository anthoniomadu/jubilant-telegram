#!/bin/bash

# Compile and run the server
echo "Compiling and running the server..."
python3 server.py --config config.json &

# Wait for the server to start
sleep 1

# Compile and run the client
echo "Compiling and running the client..."
python3 client.py --server-ip 127.0.0.1 --port 12345 --username user --password pass

# Kill the server process
kill $(jobs -p)
