# pylint: disable=missing-docstring, invalid-name, redefined-outer-name

import socket
import base64
import os
from json import loads

HOST = "localhost"
PORT = 5555
BUFFER = 1024

C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_BLUE = "\033[94m"
C_ORANGE = "\033[93m"
C_RESET = "\033[0m"

# Email data
SENDER = "amogus@localhost"
RECIPIENT = "forgetful@localhost"
IN_FILE = "in.json"

# Optional authentication
USERNAME = base64.b64encode(SENDER.encode()).decode()
PASSWORD = base64.b64encode("YourPassw0rd1H3re".encode()).decode()
USERNAME = ""
PASSWORD = ""

def readInFile():
    if not os.path.exists(IN_FILE):
        print(f"{C_RED}{IN_FILE} not found{C_RESET}")

    with open(IN_FILE, "r", encoding="utf-8") as f:
        msg = loads(f.read())
        return msg["subject"], msg["body"]

def sendEmail(verbose=False):
    subject, body = readInFile()

    msg = f"From: {SENDER}\r\nTo: {RECIPIENT}\r\nSubject: {subject}\r\n\r\n{body}\r\n"

    endmsg = "\r\n.\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        if verbose:
            print(C_ORANGE + client.recv(1024).decode() + C_RESET, end="")

        convo = [ "HELO amogus\r\n" ]

        # Optional authentication
        if USERNAME != "" and PASSWORD != "":
            convo += [
                "AUTH LOGIN\r\n",
                (USERNAME + "\r\n"),
                (PASSWORD + "\r\n")
            ]

        convo += [
            f"MAIL FROM:<{SENDER}>\r\n",
            f"RCPT TO:<{RECIPIENT}>\r\n",
            "DATA\r\n",
            (msg + endmsg),
            "QUIT\r\n"
        ]

        # conv += f"Date {datetime.now()}\r\n"

        # Manifest conversation
        for x in convo:
            client.send(x.encode())
            if verbose:
                print(x)
                print(C_ORANGE + client.recv(1024).decode() + C_RESET, end="")

if __name__ == "__main__":
    sendEmail(True)