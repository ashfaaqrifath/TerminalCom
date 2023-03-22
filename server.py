import threading
import socket
import os
import time
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

host = "192.168.8.166" # if putting public ip goes here
port = 6789
clients = []
usernames = []
connection_num = 0

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
os.system("cls")

print('''
      ▀▀█▀▀ █▀▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▄  █ █▀▀█ █     █▀▀█ █  █ █▀▀█ ▀▀█▀▀ 
        █   █▀▀▀ █▄▄▀ █ █ █  █  █ █ █ █▄▄█ █     █    █▀▀█ █▄▄█   █   
        █   █▄▄▄ █  █ █   █ ▄█▄ █  ▀█ █  █ █▄▄█  █▄▄█ █  █ █  █   █  V2.0''')
# print(Fore.LIGHTBLACK_EX +
#       "Copyright © 2023 Ashfaaq Rifath - TerminalChat")
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
                    msg6 = Fore.RED + " Command Refused"
                    client.send(msg6.encode("ascii"))

            elif msg.decode("ascii").startswith("EXIT"):
                name_to_exit = msg.decode("ascii")[5:]
                exit_user(name_to_exit)
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
                usernames.remove(username)
                break

def reciever():
    global connection_num
    while True:

        client, address = server.accept()
        client.send("USERNAME".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        
        if username == "Admin":
            client.send("ADMINPASS".encode("ascii"))
            admin_password = client.recv(1024).decode("ascii")

            if admin_password != "123":
                client.send("REFUSE".encode("ascii"))
                client.close()
                continue

        usernames.append(username)
        clients.append(client)
        connection_num += 1

        print(Fore.CYAN + f" New connection ({connection_num}) {str(address)}")
        print(Fore.YELLOW + f" Client username: {username}")
        print(Fore.GREEN + f" Connected clients: {connection_num}")

        msg3 = Fore.GREEN + f" {username} joined the server ({connection_num})"
        broadcast(msg3.encode("ascii"))
        broadcast(" ".encode("ascii"))


        msg1 = " " + Fore.BLACK + Back.GREEN + " Connected to the server " + Style.RESET_ALL
        client.send(msg1.encode("ascii"))

        msg2 = Fore.YELLOW + f" Username: {username}" + Style.RESET_ALL
        client.send(msg2.encode("ascii"))
        client.send("\n ".encode("ascii"))
        client.send("\n Type message >>".encode("ascii"))
        client.send("\n ".encode("ascii"))
        
        print()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def kick_user(name):
    global connection_num
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

def exit_user(name):
    global connection_num
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

print(" " + Fore.BLACK + Back.GREEN + " Server status: Online ")
print()
reciever()