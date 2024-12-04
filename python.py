import os
import socket
import threading

def handle_client(client_socket, addr):
    print(f"Connection established with {addr}")
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break
            if command.startswith("LIST"):
                files = "\n".join(os.listdir())
                client_socket.send(files.encode())
            elif command.startswith("UPLOAD"):
                filename = command.split()[1]
                with open(filename, "wb") as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                client_socket.send(f"{filename} uploaded.".encode())
            elif command.startswith("DOWNLOAD"):
                filename = command.split()[1]
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        client_socket.sendfile(f)
                else:
                    client_socket.send("File not found.".encode())
            elif command.startswith("DELETE"):
                filename = command.split()[1]
                if os.path.exists(filename):
                    os.remove(filename)
                    client_socket.send(f"{filename} deleted.".encode())
                else:
                    client_socket.send("File not found.".encode())
            elif command == "EXIT":
                break
    finally:
        print(f"Connection closed with {addr}")
        client_socket.close()

def start_server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
