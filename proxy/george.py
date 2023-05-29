import socket
import re

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5555

FORWARD_HOST = '127.0.0.1'
FORWARD_PORT = 5554
FORBIDDEN = {
    "very good":"plusgood",
    "very fast":"plusfast",
    "very bad":"plusungood",
    "fast":"speedful",
    "rapid":"speedful",
    "quick":"speedful",
    "slow":"unspeedful",
    "ran":"runned",
    "stole":"stealed",
    "better":"gooder",
    "best":"goodest"}

def filterForbiden(input:str):
    modify = False
    new = ""
    lines = input.split("\r\n")
    for line in lines:
        if (line == ""):
            modify = True
        if modify:
            for key,value in FORBIDDEN.items():
                regex = re.compile(re.escape(key),re.IGNORECASE)
                line = regex.sub(value,line)
        new = new + line + "\r\n"
    return new
            


proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))
proxy_socket.listen(2)
print('Proxy Server started...')
try:
    while True:
        client_socket, address = proxy_socket.accept()

        # client has connected, create a socket object for destination server
        dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest_socket.connect((FORWARD_HOST, FORWARD_PORT))
        client_data = ""
        print("client accepted")
        while True:
            # receive data from client
            recieved = client_socket.recv(4096)
            client_data += recieved.decode()
            if not recieved:
                break
        # forward data to destination server
        print("data recieved")
        client_data = filterForbiden(client_data)
        print(client_data)
        dest_socket.sendall(client_data.encode())

        # receive data from destination server
        dest_data = dest_socket.recv(4096)
        if not dest_data:
            break
        # forward data to client
        client_socket.sendall(dest_data)

        # close the client connection
        client_socket.close()
        dest_socket.close()

except KeyboardInterrupt:
    proxy_socket.close()
    dest_socket.close()
    client_socket.close()