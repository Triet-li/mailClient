
import socket, json

def getMail():
    configFile = open('config.json')
    configData = json.load(configFile)
    configFile.close()

    HOST = configData["MailServer"]
    PORT = configData["POP3"]

    # while True:
    #     print("List of folders in your mailbox: ")
    #     print("1. Inbox")
    #     print("2. Project")
    #     print("3. Important")
    #     print("4. Work")
    #     print("5. Spam")
    #     folderOption = int(input("Which folder to view email: "))
    #     if folderOption < 1 or folderOption > 5:
    #         print("Invalid input. Please choose again.")
    #     else: 
            
    #         break

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.recv(1024)
    
        user = f'USER {configData["Username"]}\r\n'
        s.sendall(user.encode())
        print(s.recv(1024).decode())

        Password = f'PASS {configData["Password"]}\r\n'
        s.sendall(Password.encode())
        print(s.recv(1024).decode())

        s.sendall(b'TOP 1 2\r\n')
        print(s.recv(1024).decode())



        s.sendall(b'QUIT\r\n')
