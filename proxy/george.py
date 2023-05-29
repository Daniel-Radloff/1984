# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
import socket
import re

C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_BLUE = "\033[94m"
C_ORANGE = "\033[93m"
C_RESET = "\033[0m"

PROXY_HOST = ""
PROXY_PORT = 5555
BUFFER = 1024

FORWARD_HOST = ""
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

def filterForbiden(inp:str):
    print("VERBODE:\n" + inp)
    modify = False
    new = ""
    lines = inp.split("\r\n")
    for line in lines:
        if line == "":
            modify = True
        if modify:
            for key,value in FORBIDDEN.items():
                regex = re.compile(re.escape(key),re.IGNORECASE)
                line = regex.sub(value,line)
        new = new + line + "\r\n"
    return new
            
def connectSocket(ip, port):
    ctrlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrlSock.connect((ip, port))

    return ctrlSock

def runProxy():
    # Create listening socket for clients
    sClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sClient.bind((PROXY_HOST, PROXY_PORT))

    # Accept incoming connections
    # TODO: Make async
    while True:
        try:
            sClient.listen(1)

            clientConn, _ = sClient.accept()
            print(C_BLUE + "="*10 + " NEW CONNECTION " + "="*10)

            # Create forwarding socket for server
            sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sServer.connect((FORWARD_HOST, FORWARD_PORT))

            data = sServer.recv(BUFFER)
            clientConn.send(data)

            # Mediate conversation
            while data := clientConn.recv(BUFFER):
                print(data.decode(), end="")

                sServer.send(data)
                resp = sServer.recv(BUFFER)

                if not resp:
                    break

                print(C_ORANGE + resp.decode() + C_RESET, end="")

                clientConn.send(resp)

        except KeyboardInterrupt:
            print(C_RED + "Keyboard interrupt" + C_RESET)
            clientConn.close()
            sServer.close()
            break

        finally:
            clientConn.close()
            sServer.close()

    sClient.close()

if __name__ == "__main__":
    runProxy()