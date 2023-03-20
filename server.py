import threading
import socket
import os
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

host = "192.168.8.166"
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

os.system("cls")

# 1.Broadcasting Method
def broadcast(message):
    for client in clients:
        client.send(message)

# 2.Recieving Messages from client then broadcasting
def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode("ascii").startswith("KICK"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_kick = msg.decode("ascii")[5:]
                    kick_user(name_to_kick)
                else:
                    client.send("Command Refused!".encode("ascii"))
            else:
                broadcast(message)   # As soon as message recieved, broadcast it.

        except:
            if client in clients:
                index = clients.index(client)
                #Index is used to remove client from list after getting diconnected
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f"{nickname} left the Chat!".encode("ascii"))
                nicknames.remove(nickname)
                break

# Main Recieve method
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        # Ask the clients for Nicknames
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        # If the Client is an Admin promopt for the password.
        

        if nickname == "admin":
            client.send("PASS".encode("ascii"))
            password = client.recv(1024).decode("ascii")
            # I know it is lame, but my focus is mainly for Chat system and not a Login System
            if password != "adminpass":
                client.send("REFUSE".encode("ascii"))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the Chat".encode("ascii"))
        client.send("Connected to the Server!".encode("ascii"))

        # Handling Multiple Clients Simultaneously
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("You Were Kicked from Chat".encode("ascii"))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f"{name} was kicked from the server".encode("ascii"))

#Calling the main method
print("Server is Listening ...")
recieve()
