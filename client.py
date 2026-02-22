# This is a python script for a client to connect to a file transfer server.

import socket
import os
import time

# Client setup to AWS server

SERVER_IP = "54.225.55.154" # Public IP address to my EC2 instance
PORT = 5000 # port indicated in EC2 instance
BUFFER_SIZE = 4096 # how much data we'll transfer at a time (4KB)
SEPARATOR = "<SEPARATOR>"

def upload_file(filename):
    # first we have to check that the desired file exists in the server
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
    filesize = os.path.getsize(filename) # gets the size of the file

    # Setting up the socket. This is the communication between client and server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # use IPv4 and TCP to communicate

    try:
        print(f"Connecting to Server | IP:{SERVER_IP} on Port:{PORT}")
        # The handshake (Transport Layer)
        client_socket.connect((SERVER_IP, PORT)) # uses public IPv4 address and port from EC2 instance as mentioned above
        print("Connected.")
        # Header
        header = f"SEND{SEPARATOR}{filename}{SEPARATOR}{filesize}"
        client_socket.send(header.encode())

        time.sleep(0.1)

        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE) # read the file in chunks of the BUFFER_SIZE which for now is 4KB
                if not bytes_read:
                    break # when all of the data from the file has been transfered, stop
                client_socket.sendall(bytes_read)

        response = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Server response: {response}")

    except Exception as error:
        print(f"Cannot connect to server: {error}") # in case client cannot establish connection to server
    finally:
        client_socket.close()

def download_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    client.send(f"GET{SEPARATOR}{filename}".encode())

    response = client.recv(BUFFER_SIZE).decode()
    if response.startswith("ERROR"):
        print(response)
    else:
        filesize = int(response)
        with open(f"downloaded_{filename}", "wb") as file:
            bytes_rec = 0
            while bytes_rec < filesize:
                chunk = client.recv(BUFFER_SIZE)
                file.write(chunk)
                bytes_rec += len(chunk)
        print(f"Downloaded {filename}")
    client.close()

if __name__ == "__main__":
    choice = input("Type U to upload a file or D to download a file: ").upper()
    fname = input("Filename: ")
    if choice == 'U':
        upload_file(fname)
    else:
        download_file(fname)