import socket, threading

def receive_message(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
    except Exception as e:
        print(f"Error receiving messages: {str(e)}")

def send_message(client_socket):
    try:
        while True:
            message = input()
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending messages: {str(e)}")

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host_name = socket.gethostname()
    # get local machine ip
    host_ip = socket.gethostbyname(host_name)
    # Reserve a port for your service.
    port = 12345

    # Connect to server
    client_socket.connect((host_ip, port))

    # start a new thread to receive message from server
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    # send message to server
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()

if __name__ == "__main__":
    main()