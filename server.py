import os
import time
import json
import threading
import socket
import colorama
import datetime
from chronicle_engine import chronicle_log, clean_slate
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

incognito = 0
clients = []
usernames = []
connection_num = 0

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
time_stamp = datetime.datetime.now().strftime("%D:%h:%H:%M:%S")

chronicle_log(write=f'''TerminalChat v2.1.5
{str(time_stamp)}
<< ACTIVITY LOG >>
IP Address: {ip}
''', incog=incognito)

def program_title():
    print('''
    ▀▀█▀▀ █▀▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▄  █ █▀▀█ █     █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
      █   █▀▀▀ █▄▄▀ █ █ █  █  █ █ █ █▄▄█ █     █    █▀▀█ █▄▄█   █   
      █   █▄▄▄ █  █ █   █ ▄█▄ █  ▀█ █  █ █▄▄▄  █▄▄█ █  █ █  █   █  v2.1.5''')
    print()
    print(Fore.LIGHTBLACK_EX + "                Copyright © Ashfaaq Rifath")
    print()

def progress(percent=0, width=30):
    symbol = width * percent // 100
    blanks = width - symbol
    print('\r[ ', Fore.GREEN + symbol * "█", blanks*' ', ' ]',
          f' {percent:.0f}%', sep='', end='', flush=True)

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

    os.system("cls")
    program_title()
    print(" " + Fore.BLACK + Back.YELLOW + " SERVER SIDE ")
    print()
    option = input(Fore.LIGHTCYAN_EX + " (1) Connect server\n (2) Add new server\n >> ")
    print()

    if option == "1":
        with open("servers.json") as f:
            data = json.load(f)
        print(Fore.CYAN + " Available servers:")

        for servers in data:
            print(" " + servers)
    
        while True:
            server_name = input(Fore.CYAN + " Select server: " + Style.RESET_ALL)
            if server_name in data:
                break
            elif server_name not in data:
                print(" " + Fore.BLACK + Back.RED + " INVALID SERVER ")
                print()

        host = data[server_name]["ip"]
        port = data[server_name]["port"]

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        break
    
    elif option == "2":
        add_server() 
    else:
        print(" " + Fore.BLACK + Back.RED+ " INVALID OPTION ")
        print()

print("")
print(Fore.YELLOW + "        Activating server")
for i in range(101):
    progress(i)
    time.sleep(0.01)

print()
print(Fore.GREEN + "          Server online")
print("")
time.sleep(1)
os.system("cls")
program_title()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    global incognito
    while True:
        try:
            msg = message = client.recv(1024)
            chronicle_log(msg.decode("ascii"), incognito)

            if msg.decode("ascii").startswith("KICK"):
                if usernames[clients.index(client)] == "Admin":
                    name_to_kick = msg.decode("ascii")[5:]
                    kick_user(name_to_kick)
                else:
                    msg6 = Fore.RED + " << Command Refused >>"
                    client.send(msg6.encode("ascii"))
                    chronicle_log(msg6, incognito)

            elif msg.decode("ascii").startswith("EXIT"):
                name_to_exit = msg.decode("ascii")[5:]
                user_exit(name_to_exit)

            elif msg.decode("ascii").startswith("INCOG"):
                chronicle_log(" << Admin enabled Incognito mode >>", incognito)
                chronicle_log("END LOG >>", incognito)
                incognito = 1
                msg8 = Fore.YELLOW + " << Admin enabled Incognito mode >>"
                print(Fore.RED + " << Admin enabled Incognito mode >>")
                print()
                broadcast(msg8.encode("ascii"))

            elif msg.decode("ascii").startswith("DISABLE"):
                incognito = 0
                msg9 = Fore.YELLOW + " << Admin disabled Incognito mode >>"
                print(Fore.RED + " << Admin disabled Incognito mode >>")
                print()
                chronicle_log(msg9, incognito)
                broadcast(msg9.encode("ascii"))

            elif msg.decode("ascii").startswith("CLEAN"):
                msg9 = Fore.YELLOW + " << Admin initiated Clean Slate Protocol >>"
                print(Fore.RED + " << Admin initiated Clean Slate Protocol >>")
                chronicle_log(msg9, incognito)
                broadcast(msg9.encode("ascii"))
                clean_slate()
                incognito = 0
                msg10 = Fore.GREEN + " All Activity log files has been deleted"
                print(Fore.YELLOW + " All Activity log files has been deleted")
                print()
                broadcast(msg10.encode("ascii"))
            else:
                broadcast(message)

        except ConnectionResetError:
            if client in clients:
                index = clients.index(client)
                client.remove(client)
                client.close
                username = usernames[index]
                msg7 = Fore.RED + f" {username} left the server"
                broadcast(msg7.encode("ascii"))
                chronicle_log(msg7, incognito)
                usernames.remove(username)
                break

def reciever():
    global connection_num
    global incognito

    while True:
        client, address = server.accept()
        client.send("USERNAME".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        
        if username == "Admin":
            client.send("ADMINPASS".encode("ascii"))
            admin_password = client.recv(1024).decode("ascii")

            if admin_password != "1234":
                client.send("REFUSE".encode("ascii"))
                client.close()
                continue 

        usernames.append(username)
        clients.append(client)
        connection_num += 1

        print(Fore.CYAN + f" New connection ({connection_num}) {str(address)}")
        print(Fore.YELLOW + f" Client username: {username}")
        print(Fore.GREEN + f" Connected clients: {connection_num}")

        chronicle_log(Fore.CYAN + f" New connection ({connection_num}) {str(address)}", incognito)
        chronicle_log(Fore.GREEN + f" Connected clients: {connection_num}", incognito)

        msg3 = Fore.GREEN + f" {username} joined the server ({connection_num})"
        broadcast(msg3.encode("ascii"))
        broadcast(" ".encode("ascii"))
        chronicle_log(msg3, incognito)

        # msg1 = " " + Fore.BLACK + Back.GREEN + " Connected to the server " + Style.RESET_ALL
        # client.send(msg1.encode("ascii"))

        msg2 = Fore.YELLOW + f" Username: {username}" + Style.RESET_ALL
        client.send(msg2.encode("ascii"))
        #client.send("\n ".encode("ascii"))
        client.send("\n Type message >>".encode("ascii"))
        client.send("\n ".encode("ascii"))
        
        print()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def kick_user(name):
    global connection_num
    global incognito

    if name in usernames:
        name_index = usernames.index(name)
        kick_client = clients[name_index]
        clients.remove(kick_client)
        connection_num -= 1
        
        msg4 = " " + Fore.BLACK + Back.RED + " You were kicked from the server by the Admin "
        kick_client.send(msg4.encode("ascii"))
        kick_client.close()

        usernames.remove(name)
        print(Fore.RED + f" {name} was kicked from the server by the Admin")
        print()
        msg5 = Fore.RED + f" {name} was kicked from the server by the Admin"
        broadcast(msg5.encode("ascii"))
        broadcast(" ".encode("ascii"))
        chronicle_log(msg5, incognito)

def user_exit(name):
    global connection_num
    global incognito

    if name in usernames:
        name_index = usernames.index(name)
        exit_client = clients[name_index]
        clients.remove(exit_client)
        connection_num -= 1

        msg8 = " " + Fore.BLACK + Back.RED + " You left the server "
        exit_client.send(msg8.encode("ascii"))
        exit_client.close()

        usernames.remove(name)
        print(Fore.RED + f" {name} left the server")
        print()
        msg5 = Fore.RED + f" {name} left the server"
        broadcast(msg5.encode("ascii"))
        chronicle_log(msg5, incognito)

print(Fore.GREEN + f" Connected server: {server_name} " + Style.RESET_ALL)
print(" " + Fore.BLACK + Back.GREEN + " Server status: Online ")
print()
reciever()


# Copyright © 2023 Ashfaaq Rifath - TerminalChat v2.0.5