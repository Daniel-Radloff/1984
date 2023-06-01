# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
import socket
from datetime import datetime
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

BLACKLIST = { "email": [], "ip": [] }

# All tokens are equal, but some are more equal than others if they're declared earlier
FORBIDDEN = {
    "illuminati": "",
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
    "best":"goodest"
}

DISCLAIMER = "\r\n\r\nPlease do not take anything in this email seriously!"

# A mini tokenizer to check for disallowed words
def ingsoc(inp:str):
    # substring replacement that maintains capitalization
    def smartReplace(index, token, replacement):
        oldWord = inp[index:index+len(token)]

        if oldWord.islower():
            return replacement
        if oldWord.isupper():
            return replacement.upper()
        if oldWord.istitle():
            return replacement.title()

        return replacement

    def wordMatch(token, index):
        # abcde
        # 1 + 3
        lastCharIndex = index + len(token) - 1
        if lastCharIndex >= len(inp):
            return False

        # Check we have a char-for-char match
        for i, c in enumerate(token):
            if c != inp[index + i].lower():
                return False

        # Check its not a subword
        splitterChars = " \t\n,.;-:()}{[]_?!"
        if index > 0:
            if not inp[index-1] in splitterChars:
                return False

        if lastCharIndex+1 < len(inp):
            if not inp[lastCharIndex+1] in splitterChars:
                return False
        
        # Handle special illuminati case
        if token == "illuminati":
            return token
        
        return True

    res = ""
    i = 0
    while i < len(inp):
        foundToken = False
        for k, v in FORBIDDEN.items():
            isMatch = wordMatch(k, i)
            if isMatch == "illuminati":
                return "Hello world"
            if isMatch:
                # Replace substring + skip ahead
                res += smartReplace(i, k, v)
                i += len(k)
                foundToken = True
                break

        if not foundToken:
            res += inp[i]
            i += 1

    return res

# Split a `DATA` payload into header and message (w/o termination seq.)
def splitPayload(data):
    # TODO: We might wanna check for tags like `From:`, `To:`, `Subject:`
    #       at the beginning of lines to more accurately delineate headers/body
    arr = data.split("\r\n\r\n")

    if len(arr) == 0:   return "", ""
    elif len(arr) == 1: return "", "\r\n\r\n".join(arr[0:-1])
    else:               return arr[0], "\r\n\r\n".join(arr[1:-1])

def splitHeaders(headers):
    return [h.split(":") for h in headers.split("\r\n")]

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

            clientConn, addr = sClient.accept()
            # Check blacklist
            print("ADDRESS:", addr)
            if checkBlacklist(addr[0], "ip"):
                clientConn.close()
                raise Exception("IP [" + addr[0] + "] blacklisted")

            print(C_BLUE + "="*10 + " NEW CONNECTION " + "="*10)

            # Create forwarding socket for server
            sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sServer.connect((FORWARD_HOST, FORWARD_PORT))

            data = sServer.recv(BUFFER)
            clientConn.send(data)

            sendingMessageBody = False

            # Mediate conversation
            while cmd := clientConn.recv(BUFFER):
                sCmd = cmd.decode()

                # Check for actual message body (after `DATA`)
                if sendingMessageBody:
                    # For debugging
                    with open("test1.txt", "w", encoding="utf-8") as f:
                        f.write(sCmd)
                    headers, body = splitPayload(sCmd)
                    sCmd = headers + "\r\n\r\n" + ingsoc(body) + DISCLAIMER + "\r\n.\r\n"
                    with open("test2.txt", "w", encoding="utf-8") as f:
                        f.write(sCmd)
                    sendingMessageBody = False

                elif sCmd.startswith("DATA"):
                    print(C_RED + "SENDING DATA NOW" + C_RESET)
                    sendingMessageBody = True

                print(sCmd, end="")

                sServer.send(sCmd.encode())
                resp = sServer.recv(BUFFER)

                if not resp: # If server terminates conn.
                    break

                print(C_ORANGE + resp.decode() + C_RESET, end="")

                clientConn.send(resp)

        except KeyboardInterrupt:
            print(C_RED + "Keyboard interrupt" + C_RESET)
            if "clientConn" in locals():  clientConn.close()
            if "sServer" in locals():     sServer.close()
            break

        except Exception as e:
            print(C_RED + "Exception: " + str(e) + C_RESET)

        finally:
            if "clientConn" in locals():  clientConn.close()
            if "sServer" in locals():     sServer.close()

    sClient.close()

# Returns true if the specified value is blacklisted
def checkBlacklist(value, valType):
    for v in BLACKLIST[valType]:
        if value.lower() == v["value"]:
            if v["expiryTime"] == -1 or v["expiryTime"] > datetime.now().timestamp():
                return True
    return False

def loadBlacklist():
    # Read blacklist
    with open("blacklist", "r", encoding="utf-8") as f:
        for line in f:
            row = line.split()
            value = row[0].strip()
            expiryTime = -1 # never expires
            try: expiryTime = int(row[1].strip())
            except: expiryTime = -1

            if re.match(r"^\S+@\S+\.\w+$", value):
                BLACKLIST["email"].append({
                    "value": value.lower(),
                    "expiryTime": expiryTime
                })
            elif re.match(r"^(\d{1,3}[:.]){3}\d{1,3}(\/\d\d?)?$", value):
                BLACKLIST["ip"].append({
                    "value": value.replace(":", ".").split("/")[0],
                    "expiryTime": expiryTime
                })

if __name__ == "__main__":
    loadBlacklist()
    runProxy()
