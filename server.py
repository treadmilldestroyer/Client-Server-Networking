import socket
import os
import time

# Server Configuration
IP = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def start_server():
    # Create the TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This allows us to restart the server without "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print(f"[*] Server listening on {PORT}...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] {address} is connected.")

        try:
            # Receive the initial command from the client
            message = client_socket.recv(BUFFER_SIZE).decode()
            if not message:
                continue

            # allows us to download files
            if message.startswith("GET"):
                _, filename = message.split(SEPARATOR)
                if os.path.exists(filename):
                    filesize = os.path.getsize(filename)
                    # Send the size first
                    client_socket.send(f"{filesize}".encode())
                    
                    # Wait 0.1 seconds so the size and data don't arrive at the client at the same time.
                    time.sleep(0.1)
                    
                    with open(filename, "rb") as f:
                        while True:
                            chunk = f.read(BUFFER_SIZE)
                            if not chunk: 
                                break
                            client_socket.sendall(chunk)
                    print(f"[+] Successfully sent {filename} to client.")
                else:
                    client_socket.send(b"ERROR: File not found")

            # allows us to upload files
            elif message.startswith("SEND"):
                _, filename, filesize = message.split(SEPARATOR)
                filename = os.path.basename(filename)
                filesize = int(filesize)
                
                print(f"[!] Receiving: {filename}...")
                with open(f"received_{filename}", "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        chunk = client_socket.recv(BUFFER_SIZE)
                        if not chunk: 
                            break
                        f.write(chunk)
                        bytes_received += len(chunk)
                
                print(f"[+] File {filename} saved successfully.")
                client_socket.send(b"Upload complete.")

        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            client_socket.close()
            print(f"[-] Connection with {address} closed.\n")

if __name__ == "__main__":
    start_server()