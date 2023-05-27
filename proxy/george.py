import socket

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5555

FORWARD_HOST = '127.0.0.1'
FORWARD_PORT = 5554

proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))
proxy_socket.listen(2)
print('Proxy Server started...')
client_socket, address = proxy_socket.accept()

# client has connected, create a socket object for destination server
dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_socket.connect((FORWARD_HOST, FORWARD_PORT))

while True:
    # receive data from client
    client_data = client_socket.recv(4096)
    if not client_data:
        break
    # forward data to destination server
    dest_socket.sendall(client_data)

    # receive data from destination server
    dest_data = dest_socket.recv(4096)
    if not dest_data:
        break
    # forward data to client
    client_socket.sendall(dest_data)

# close the client connection
client_socket.close()

# close the server sockets
proxy_socket.close()
dest_socket.close()
