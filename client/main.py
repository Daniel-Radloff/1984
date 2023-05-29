import socket
from datetime import datetime
from dateutil.relativedelta import relativedelta

host:str = "127.0.0.1"
port:int = 5555
template:str = "in.txt"

def sendData(message:str, client:socket):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(e)

def sendSMTP(message:str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port))
    sendData("helo localhost\r\n",client)
    sendData("mail from: myself@radloff.gd\r\n",client)
    sendData("rcpt to: gustav@radloff.gd\r\n",client)
    sendData("data\r\n",client)
    sendData("From: fake@fake.fake\r\n",client)
    sendData("To: you@are@a@clown.clown.clown.clown\r\n",client)
    sendData("Subject: Reminder\r\n",client)
    sendData("Received: from bar.com by foo.com ; Thu, 21 May 1998 05:33:29 -0700 credit to the rfc for this one\r\n",client)
    sendData("\r\n",client)
    sendData(message,client)
    sendData("\r\n",client)
    sendData(".\r\n",client)
    client.sendall("quit\r\n".encode())
    client.close()


def main():
    toSend = ""
    with open(template,'r') as fileHandle:
        for line in fileHandle:
            toSend = toSend + line
    sendSMTP(toSend)

main()
