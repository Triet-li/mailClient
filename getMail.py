
import socket, json
import os

configFile = open('config.json')
configData = json.load(configFile)
configFile.close()

HOST = configData["MailServer"]
PORT = configData["POP3"]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(1024)
 
    user = f'USER {configData["Username"]}\r\n'
    s.sendall(user.encode())
    print(s.recv(1024).decode())

    Password = f'PASS {configData["Password"]}\r\n'
    s.sendall(Password.encode())
    print(s.recv(1024).decode())

    s.sendall(b'RETR 2\r\n')
    print(s.recv(1024).decode())



    s.sendall(b'QUIT\r\n')
