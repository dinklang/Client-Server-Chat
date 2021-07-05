import socket
import sys

HEADER_LENGTH = 10
PORT = 5100

name = socket.gethostname()

my_username = input("Name: ")

# Create a socket
client_socket = socket.socket() 

# Connect to port
client_socket.connect((name, PORT))

# Exception
client_socket.setblocking(False)

# Encode and send username
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    # User input
    message = input(f'{my_username} > ')

    # Check for message
    if message:
        # Encode and send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # decode
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Display
            print(f'{username} > {message}')

    except IOError as e:
        pass