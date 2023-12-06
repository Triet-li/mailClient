
import socket

HOST = "127.0.0.1"
PORT = 22345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    welcome_msg = s.recv(1024)
    print(welcome_msg.decode())

    s.sendall(b'EHLO 127.0.0.1\r\n')
    ehlo_response = s.recv(1024)
    print(ehlo_response.decode())

     # Send the MAIL FROM and RCPT TO commands
    s.sendall(b'MAIL FROM:triethouse@gmail.com\r\n')
    s.sendall(b'RCPT TO:triethouse@gmail.com\r\n')

    s.sendall(b'DATA\r\n')
    data_response = s.recv(1024)
    print(data_response.decode())

    s.sendall(b'Subject: ok bro\r\n\r\nhehehehehehhehe\r\n.\r\n')

     # Quit the session
    s.sendall(b'QUIT\r\n')
    quit_response = s.recv(1024)
    print(quit_response.decode())


