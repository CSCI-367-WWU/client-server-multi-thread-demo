import socket, threading

# create a list to store all the client sockets
clients = []
# create a lock to prevent race condition on the clients list
lock = threading.Lock()

# handle a single client on a separate thread
def client_handler(client_socket, client_addr):
    # add the client socket to the list with a lock
    with lock:
        clients.append(client_socket)
    
    # send a welcome message to the client
    client_socket.send("Welcome to the chat room!\n".encode())

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Client {client_addr}: {message}")
            broadcast(message, client_socket)
    except:
        print(f"Error handling client: {client_addr}")
    finally:
        with lock:
            clients.remove(client_socket)
        client_socket.close()
        print(f"Client {client_addr} has disconnected")

# broadcast a message to all clients except the sender
def broadcast(message, client_socket):
    with lock:
        for client in clients:
            if client != client_socket:
                client.send(message.encode())

# main function
def main():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # necessary variables
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 12345

    # bind to the port
    server.bind((host_ip, port))
    # listen for incoming connections
    server.listen()
    
    print(f"Server is listening on {host_ip}:{port}")

    while True:
        # establish a connection
        client, client_addr = server.accept()
        print(f"Got a connection from {client_addr}")
        clinet_socket = threading.Thread(target=client_handler, args=(client, client_addr))
        clinet_socket.start()

if __name__ == "__main__":
    main()