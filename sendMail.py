
import socket, json
import datetime
import base64
def sendMail():

    configFile2 = open('sender.json')
    sender = json.load(configFile2)["sender"]
    configFile2.close()

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
    numOfAttachFiles = 0
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
        mailFromUser = f'MAIL FROM:{sender}\r\n'
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

        # Construct MIME-formatted email
        email_data = f"To: {', '.join(emailTo)}\r\n"
        email_data +=  f"Cc: {','.join(emailCC)}\r\n"
        email_data += f"From: {configData['Username']}\r\n"
        email_data += f"Subject: {subject}\r\n"
        email_data += f"Date: abc\r\n"
        #email_data += "MIME-Version: 1.0\r\n"
        email_data += "Content-Type: multipart/mixed;\r\n boundary=myboundary\r\n"

        # Text part
        email_data += "--myboundary\r\n"
        email_data += "Content-Type: text/plain\r\n\r\n"
        #email_data += "Content-Transfer-Encoding: 7bit\r\n\r\n"
        email_data += f"{content}\r\n\r\n"

        # Attach file ( base64 )
        if numOfAttachFiles > 0:
            filesExtension = []
            for i in path2AttachFiles:
                if i.endswith('.docx'): 
                    filesExtension.append('docx')
                elif i.endswith('.pdf'):
                    filesExtension.append('pdf')
                elif i.endswith('.jpg'):
                    filesExtension.append('jpg')
                elif i.endswith('.zip'):
                    filesExtension.append('zip')
                elif i.endswith('.txt'):
                    filesExtension.append('txt')

        # Closing boundary
        email_data += "--myboundary\r\n"
        email_data += ".\r\n"

        # e = [ f"To: {','.join(emailTo)}", f"CC: {','.join(emailCC)}",  f"From: {configData['Username']}",
        #      f"Subject: {subject}", "\r\n", f'{content}\r\n.\r\n', f"Date: abc", f"MIME-Version: 1.0"]
        # email = "\n".join(e)
        
     

        s.sendall(email_data.encode())
        ok = s.recv(1024)
        
        print("\nSent\n")
        # Quit the session
        s.sendall(b'QUIT\r\n')
        quit_response = s.recv(1024)


