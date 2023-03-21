import threading
import socket
import os
import time
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

host = "192.168.8.166"
port = 6789
clients = []
usernames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def progress(percent=0, width=30):
    symbol = width * percent // 100
    blanks = width - symbol
    print('\r[ ', Fore.GREEN + symbol * "█", blanks*' ', ' ]',
          f' {percent:.0f}%', sep='', end='', flush=True)


print("")
print(Fore.YELLOW + "        Initiating server")
for i in range(101):
    progress(i)
    time.sleep(0.01)

print()
print(Fore.GREEN + "         Server activated")
print("")
print(Fore.LIGHTBLACK_EX +
      "Copyright © 2023 Ashfaaq Rifath - TerminalChat")
time.sleep(1)
os.system('cls')

print('''
        ▀▀█▀▀ █▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▀▀▄ █▀▀█ █    █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
          █   █▀▀ █▄▄▀ █ ▀ █  █  █  █ █▄▄█ █    █    █▀▀█ █▄▄█   █    
          █   ▀▀▀ ▀ ▀▀ ▀   ▀ ▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀  █▄▄█ ▀  ▀ ▀  ▀   ▀ V2.0''')
print()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode("ascii").startswith("KICK"):
                if usernames[clients.index(client)] == "Admin":
                    name_to_kick = msg.decode("ascii")[5:]
                    kick_user(name_to_kick)
                else:
                    client.send(" Command Refused".encode("ascii"))
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                client.remove(client)
                client.close
                username = usernames[index]
                broadcast(f" {username} left the server".encode("ascii"))
                usernames.remove(username)
                break

def recieve():
    num = 0
    while True:

        client, address = server.accept()
        client.send("USERNAME".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        
        if username == "Admin":
            client.send("ADMINPASS".encode("ascii"))
            admin_password = client.recv(1024).decode("ascii")

            if admin_password != "admin123":
                client.send("REFUSE".encode("ascii"))
                client.close()
                continue

        usernames.append(username)
        clients.append(client)
        num += 1

        print(Fore.CYAN + f" New connection ({num}) {str(address)}")
        print(Fore.YELLOW + f" Client username: {username}")

        print(Fore.GREEN + f" {username} joined the server")
        msg3 = Fore.GREEN + f" {username} joined the server"
        broadcast(msg3.encode("ascii"))


        msg1 = " " + Fore.BLACK + Back.GREEN + " Connected to the server " + Style.RESET_ALL
        client.send(msg1.encode("ascii"))

        msg2 = Fore.CYAN + f" Username: {username}" + Style.RESET_ALL
        client.send(msg2.encode("ascii"))
        client.send("\n ".encode("ascii"))
        client.send("\n Type message >>".encode("ascii"))
        client.send("\n ".encode("ascii"))
        
        print()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def kick_user(name):
    if name in usernames:
        name_index = usernames.index(name)
        kick_client = clients[name_index]
        clients.remove(kick_client)

        msg4 = Fore.RED + " You were kicked from the server"
        kick_client.send(msg4.encode("ascii"))
        kick_client.close()

        usernames.remove(name)
        print(Fore.RED + f" {name} was kicked from the server")
        print()
        msg5 = Fore.RED + f" {name} was kicked from the server"
        broadcast(msg5.encode("ascii"))

print(" " + Fore.BLACK + Back.GREEN + " Server is online ")
print()
recieve()