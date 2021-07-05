import socket
import select

HEADER_LENGTH = 10
PORT = 5100

name = socket.gethostname()

# Create a socket
server_socket = socket.socket()

# Bind information to port
server_socket.bind((name, PORT))

# Listen to new connections
server_socket.listen()

# List of sockets
sockets_list = [server_socket]

# List of clients
clients = {}

print(f'{name}:{PORT} is waiting for connections')

# Receive messages
def receive_message(client_socket):
    message_header = client_socket.recv(HEADER_LENGTH)

    if not len(message_header):
        return False

    # Convert header to int value
    message_length = int(message_header.decode('utf-8').strip())

    # Return message data
    return {'header': message_header, 'data': client_socket.recv(message_length)}

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        # If CLIENT is trying to join, accept.
        if notified_socket == server_socket:

            # Accept CLIENT connection and info
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            # Check if client disconnected
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Check for messages after connection
        else:
            message = receive_message(notified_socket)
            # Check if CLIENT disconnected
            if message is False:
                print('{} logged out.'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            # Get user info and display message
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Go through connected clients
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
