import socket
import threading
import json
import os
import time
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)


os.system("cls")

print('''
        ▀▀█▀▀ █▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▀▀▄ █▀▀█ █    █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
          █   █▀▀ █▄▄▀ █ ▀ █  █  █  █ █▄▄█ █    █    █▀▀█ █▄▄█   █  
          █   ▀▀▀ ▀ ▀▀ ▀   ▀ ▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀  █▄▄█ ▀  ▀ ▀  ▀   ▀ ''')
print()

def progress(percent=0, width=30):
    symbol = width * percent // 100
    blanks = width - symbol
    print('\r[ ', Fore.GREEN + symbol * "█", blanks*' ', ' ]',
          f' {percent:.0f}%', sep='', end='', flush=True)

def enter_server():
    global username
    global admin_password
    global client

    with open("servers.json") as f:
        data = json.load(f)
    print(" Your servers: ", end = "")
    for servers in data:
        print(" " + servers, end = " ")
    server_name = input("\n Enter the server name: ")

    username = input(" Choose your username: ").capitalize()
    if username == "Admin":
        admin_password = input(" Enter admin password: ")

    ip = data[server_name]["ip"]
    port = data[server_name]["port"]
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip,port))

def add_server():
    os.system("cls")
    server_name = input(" Enter a name for the server: ")
    server_ip = input(" Enter the ip address of the server: ")
    server_port = int(input(" Enter the port number of the server: "))

    with open("servers.json", "r") as f:
        data = json.load(f)

    with open("servers.json", "w") as f:
        data[server_name] = {"ip": server_ip, "port": server_port}
        json.dump(data, f, indent=4)

while True:
    option = input(" (1)Enter server\n (2)Add server\n >> ")
    if option == "1":
        enter_server()
        break
    elif option == "2":
        add_server() 

stop_thread = False

def recieve_msg():
    print()
    print(Fore.YELLOW + "        Connecting server")
    for i in range(101):
        progress(i)
        time.sleep(0.01)
    print()
    print(Fore.GREEN + "         Succesfull")
    os.system("cls")

    print('''
            ▀▀█▀▀ █▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▀▀▄ █▀▀█ █    █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
              █   █▀▀ █▄▄▀ █ ▀ █  █  █  █ █▄▄█ █    █    █▀▀█ █▄▄█   █  
              █   ▀▀▀ ▀ ▀▀ ▀   ▀ ▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀  █▄▄█ ▀  ▀ ▀  ▀   ▀ ''')
    print()
    while True:
        global stop_thread

        if stop_thread:
            break
        try:
            message = client.recv(1024).decode("ascii")
            if message == "USERNAME":
                client.send(username.encode("ascii"))
                next_message = client.recv(1024).decode('ascii')

                if next_message == "ADMINPASS":
                    client.send(admin_password.encode("ascii"))

                    if client.recv(1024).decode("ascii") == "REFUSE":
                        print(" Connection is Refused. Wrong Password")
                        stop_thread = True
            else:
                print(Fore.MAGENTA + message)
        except:
            print(" Error Occured while Connecting")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{username}: {input("")}'

        if message[len(username)+2:].startswith("/"):
            if username == "Admin":
                if message[len(username)+2:].startswith("/kick"):
                    client.send(f"KICK {message[len(username)+2+6:]}".encode("ascii"))
            else:
                print(Fore.RED + " Commands can be executed by Admins only")
        else:
            show_msg = Fore.LIGHTCYAN_EX + " " + message
            client.send(show_msg.encode("ascii"))
            client.send(" ".encode("ascii"))

recieve_thread = threading.Thread(target=recieve_msg)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()