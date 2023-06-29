import socket
import threading
import json
import os
import time
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

os.system("cls")

print('''
      ▀▀█▀▀ █▀▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▄  █ █▀▀█ █     █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
        █   █▀▀▀ █▄▄▀ █ █ █  █  █ █ █ █▄▄█ █     █    █▀▀█ █▄▄█   █   
        █   █▄▄▄ █  █ █   █ ▄█▄ █  ▀█ █  █ █▄▄█  █▄▄█ █  █ █  █   █  v2.0.3 ''')
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
    print(Fore.CYAN + " Available servers:")

    for servers in data:
        print(" " + servers)
    server_name = input(Fore.CYAN + " Enter the server name: " + Style.RESET_ALL)
    if server_name not in data:
        print(" " + Fore.BLACK + Back.RED+ " Invalid server ")

    try:
        username = input(Fore.YELLOW + " Choose your username: " + Style.RESET_ALL).capitalize()
        if username == "Admin":
            admin_password = input(" Enter admin password: ")

        ip = data[server_name]["ip"]
        port = data[server_name]["port"]
    except KeyError:
        print()
        print(" " + Fore.BLACK + Back.RED+ " Server does not exist ")
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip,port))
    except ConnectionRefusedError:
        print()
        print(" " + Fore.BLACK + Back.RED+ " Server status: Offline ")

def add_server():
    server_name = input(Fore.YELLOW + " Enter name for the server: ")
    server_ip = input(Fore.CYAN + " Enter IP address of the server: ")
    server_port = int(input(" Enter port number of the server: "))
    print()

    with open("servers.json", "r") as f:
        data = json.load(f)

    with open("servers.json", "w") as f:
        data[server_name] = {"ip": server_ip, "port": server_port}
        json.dump(data, f, indent=4)

while True:
    option = input(Fore.LIGHTCYAN_EX + " (1) Enter server\n (2) Add server\n >> ")
    print()
    if option == "1":
        enter_server()
        break
    elif option == "2":
        add_server() 
    else:
        print(" " + Fore.BLACK + Back.RED+ " Invalid option ")
        print()

stop_thread = False

def reciever():
    print()
    print(Fore.YELLOW + "        Connecting to server")
    for i in range(101):
        progress(i)
        time.sleep(0.01)
    os.system("cls")

    print('''
      ▀▀█▀▀ █▀▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▄  █ █▀▀█ █     █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
        █   █▀▀▀ █▄▄▀ █ █ █  █  █ █ █ █▄▄█ █     █    █▀▀█ █▄▄█   █   
        █   █▄▄▄ █  █ █   █ ▄█▄ █  ▀█ █  █ █▄▄█  █▄▄█ █  █ █  █   █  v2.0.4 ''')
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
                        print(" " + Fore.BLACK + Back.RED + " Wrong password ")
                        print(Fore.RED + " << Connection refused >>")
                        stop_thread = True
            else:
                print(message)
        except :
            print(Fore.RED + " << Server connection error >>")
            client.close()
            break

def send_msg():
    while True:
        if stop_thread:
            break
        message = f'{username}: {input("")}'

        if message[len(username)+2:].startswith("/"):
            if username == "Admin":
                if message[len(username)+2:].startswith("/kick"):
                    kick_user = message[len(username)+2+6:].capitalize()
                    client.send(f"KICK {kick_user}".encode("ascii"))
                
                elif message[len(username)+2:].startswith("/incog"):
                    client.send("INCOG".encode("ascii"))

                elif message[len(username)+2:].startswith("/dis"):
                    client.send("DISABLE".encode("ascii"))

                elif message[len(username)+2:].startswith("/del"):
                    client.send("CLEAN".encode("ascii"))
            else:
                print(Fore.RED + " << This command can be executed by Admins only >>")
                print()

        elif message[len(username)+2:].startswith("\exit"):
            client.send(f"EXIT {username}".encode("ascii"))

        else:
            show_msg = Fore.LIGHTCYAN_EX + " " + message
            client.send(show_msg.encode("ascii"))
            client.send(" ".encode("ascii"))

recieve_thread = threading.Thread(target=reciever)
recieve_thread.start()

write_thread = threading.Thread(target=send_msg)
write_thread.start()




# Copyright (c) 2023 Ashfaaq Rifath - TerminalChat v2.0.4