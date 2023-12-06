
import socket

HOST = "127.0.0.1"
PORT = 22212


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(1024)

    s.sendall(b'USER triethouse@gmail.com\r\n')
    print(s.recv(1024).decode())

    s.sendall(b'PASS trietpro2\r\n')
    print(s.recv(1024).decode())

    s.sendall(b'RETR 2\r\n')
    print(s.recv(1024).decode())



    s.sendall(b'QUIT\r\n')
