
import socket, json

configFile = open('config.json')
configData = json.load(configFile)
configFile.close()

HOST = configData["MailServer"]
PORT = configData["SMTP"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    welcome_msg = s.recv(1024)
    print(welcome_msg.decode())

    s.sendall(b'EHLO 127.0.0.1\r\n')
    ehlo_response = s.recv(1024)
    print(ehlo_response.decode())

     # Send the MAIL FROM and RCPT TO commands
    mailFromUser = f'MAIL FROM:{configData["Username"]}\r\n'
    s.sendall(mailFromUser.encode())
    s.sendall(b'RCPT TO:triethouse@gmail.com\r\n')

    s.sendall(b'DATA\r\n')
    data_response = s.recv(1024)
    print(data_response.decode())

    s.sendall(b'Subject: deo ok nha bro\r\n\r\hahahha\r\n.\r\n')

     # Quit the session
    s.sendall(b'QUIT\r\n')
    quit_response = s.recv(1024)
    print(quit_response.decode())


