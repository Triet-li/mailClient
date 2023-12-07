
import socket, json
import datetime
def sendMail():
    configFile = open('config.json')
    configData = json.load(configFile)
    configFile.close()

    HOST = configData["MailServer"]
    PORT = configData["SMTP"]

    print("Fill in the information: (press enter to skip)")
    emailTo = input("To: ").split(sep=',')
    emailCC = input("CC: ").split(sep=',')
    emailBCC = input("BCC: ").split(sep=',')
    subject = input("Subject: ")
    content = input("Content: ")
    hasAttachFiles = int(input("Has attach files? (1. yes, 2. no): "))
    path2AttachFiles = []
    if hasAttachFiles == 1:
        numOfAttachFiles = int(input("How many: "))
        for i in range(numOfAttachFiles):
            path = input(f"Path to file {i+1}: ")
            path2AttachFiles.append(path)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        welcome_msg = s.recv(1024)
        #print(welcome_msg.decode())

        s.sendall(b'EHLO 127.0.0.1\r\n')
        ehlo_response = s.recv(1024)

        # mail from
        mailFromUser = f'MAIL FROM:{configData["Username"]}\r\n'
        s.sendall(mailFromUser.encode())

        # mail to
        for i in emailTo:
            i = i.strip()
            e = f'RCPT TO:{i}\r\n'
            s.sendall(e.encode())
            s.recv(1024)

        for i in emailCC:
            i = i.strip()
            e = f'RCPT TO:{i}\r\n'
            s.sendall(e.encode())
            s.recv(1024)

        for i in emailBCC:
            i = i.strip()
            e = f'RCPT TO:{i}\r\n'
            s.sendall(e.encode())
            s.recv(1024)


        # mail content
        s.sendall(b'DATA\r\n')
        data_response = s.recv(1024)

        e = [f"Subject: {subject}", f"To: {','.join(emailTo)}", f"CC: {','.join(emailCC)}", 
             f"From: {configData['Username']}", "\r\n", f'{content}\r\n.\r\n']
        email = "\n".join(e)
        
     
        # {content}\r\n.\r\n'''
        s.sendall(email.encode())
        ok = s.recv(1024)
        
        print("\nSent\n")
        # Quit the session
        s.sendall(b'QUIT\r\n')
        quit_response = s.recv(1024)


