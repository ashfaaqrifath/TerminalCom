import socket
import threading
import json
import os
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)


def enter_server():
    global nickname
    global password
    global client

    os.system("cls")
    with open("servers.json") as f:
        data = json.load(f)
    print("Your servers: ", end = "")
    for servers in data:
        print(servers, end = " ")
    server_name = input("\nEnter the server name:")

    nickname = input("Choose Your Nickname: ")
    if nickname == "admin":
        password = input("Enter admin password: ")

    ip = data[server_name]["ip"]
    port = data[server_name]["port"]
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip,port))

def add_server():
    os.system("cls")
    server_name = input("Enter a name for the server: ")
    server_ip = input("Enter the ip address of the server: ")
    server_port = int(input("Enter the port number of the server: "))

    with open("servers.json", "r") as f:
        data = json.load(f)

    with open("servers.json", "w") as f:
        data[server_name] = {"ip": server_ip, "port": server_port}
        json.dump(data, f, indent=4)

while True:
    os.system("cls")

    option = input("(1)Enter server\n(2)Add server\n")
    if option == "1":
        enter_server()
        break
    elif option == "2":
        add_server()

stop_thread = False

def recieve_msg():
    while True:
        global stop_thread

        if stop_thread:
            break
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
                next_message = client.recv(1024).decode('ascii')

                if next_message == "PASS":
                    client.send(password.encode("ascii"))

                    if client.recv(1024).decode('ascii') == "REFUSE":
                        print("Connection is Refused. Wrong Password")
                        stop_thread = True
            else:
                print(message)
        except:
            print("Error Occured while Connecting")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break

        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith("/"):
            if nickname == "admin":
                if message[len(nickname)+2:].startswith("/kick"):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
            else:
                print("Commands can be executed by Admins only!")
        else:
            client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve_msg)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
