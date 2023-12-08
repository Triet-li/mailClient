
import socket, json
import os
from pathlib import Path
import re

MailBoxFolders = ['', 'Inbox', 'Project', 'Important', 'Work', 'Spam']
MYPATH = os.getcwd()

def parseMIME(response):
    emailHeader = response.split('\n')[1:6]
    boundary = response.split('\n')[7:8]
    boundary = ''.join(boundary).split('=')[1]
    emailContent = response.split(f'--{boundary}')[1][1:]
    return [emailHeader, emailContent]

def createFile(emailHeader, emailContent):
    filename = f'{emailHeader[2][6:]}_{emailHeader[3][9:]}.msg'
    filename = filename.replace(" ", "-")
    f = open(f'{filename}', 'w')
    for i in range(len(emailHeader)):
        f.write(f'{emailHeader[i]}\n')
    #f.write('\n')
    for i in range(len(emailContent)):
        f.write(f'{emailContent[i]}')
    
    f.close()
def sortEmail(s, mailboxName):
    os.chdir(f'{mailboxName}')
    f = open('numberOfEmails.txt', "r")
    os.chdir(MYPATH)
    numOfCurrentEmails = int(f.read())
    f.close()
    s.sendall(b'STAT\r\n')

    numOfMailOnServer =  int(s.recv(1024).decode()[4])
 
    ans = 2
    if numOfMailOnServer - numOfCurrentEmails > 0:
        ans = int(input(f'There are {numOfMailOnServer-numOfCurrentEmails} emails not downloaded yet. Do you want to download them? (1.yes, 2.no): '))
    if ans == 1:
        for i in range(numOfCurrentEmails+1, numOfMailOnServer+1):
            data = f'RETR {i}\r\n'
            s.sendall(data.encode())
            response = s.recv(1024).decode()
            res = parseMIME(response)
            emailFrom = res[0][2]
            emailSubject = res[0][3]
            emailContent = res[1]
            if 'ahihi@testing.com' in emailFrom or 'ahuu@testing.com' in emailFrom:
                os.chdir(f'{mailboxName}')
                os.chdir('Project')
                createFile(res[0], emailContent)
                os.chdir(MYPATH)
            elif 'urgent' in emailSubject or 'ASAP' in emailSubject:
                os.chdir(f'{mailboxName}')
                os.chdir('Important')
                createFile(res[0], emailContent)
                os.chdir(MYPATH)

            elif 'report' in emailContent or 'meeting' in emailContent:
                os.chdir(f'{mailboxName}')
                os.chdir('Work')
                createFile(res[0], emailContent)
                os.chdir(MYPATH)
               
            elif 'virus' in emailSubject or 'hack' in emailSubject or 'crack' in emailSubject or 'virus' in emailContent or 'hack' in emailContent or 'crack' in emailContent:
                os.chdir(f'{mailboxName}')
                os.chdir('Spam')
                createFile(res[0], emailContent)
                os.chdir(MYPATH)

            else:
               # os.chdir(f'{mailboxName}')
                os.chdir('triethouse')
                os.chdir('Inbox')
                createFile(res[0], emailContent)
                os.chdir(MYPATH)

        
        os.chdir(f'{mailboxName}')
        print("Successfully downloaded new emails.")
        f = open('numberOfEmails.txt', 'w')
        f.write(str(numOfMailOnServer))
        f.close()
        os.chdir(MYPATH)

        # count = 0
        # os.chdir(f'{mailboxName}')
        # os.chdir(f'{MailBoxFolders[folderOption]}')
        # mails = [i for i in os.listdir() if i.endswith('.msg')]


# traverse a list of files to get name
def getEmailName(s, mailboxName, folderOption):
    os.chdir(f'{mailboxName}')
    os.chdir(f'{folderOption}')

   


def viewEmailFolder(s, mailboxName, folderOption):
    os.chdir(f'{mailboxName}')
    os.chdir(f'{MailBoxFolders[folderOption]}')
    numOfMails = len(list(Path('.').glob('*.msg')))
    if not os.path.exists('checkRead.json'):
        data = {}
        for i in range(numOfMails):
            data[i] = False
        
        with open('checkRead.json', 'w') as file:
            json.dump(data, file)
    
    check = open('checkRead.json', 'r')
    checkRead = json.load(check)
    check.close()
    # os.chdir(MYPATH)
    # for i in range(numOfMails):
    #     if not i in checkRead.keys():
    #         data[i] = False
    #         json.dump(data, check)
    #         print(f'{i+1}. (not read) {getEmailName(s)}')
    #     elif checkRead[i] == False:
    #         print(f'{i+1}. (not read) {getEmailName(s)}')
    #     elif checkRead[i] == True:
    #         print(f'{i+1}. {getEmailName(s)}')
    count = 0
    #print(os.getcwd())
    #for msg in list(Path('.').glob('*.msg')):
    mails = [i for i in os.listdir() if i.endswith('.msg')]
    mails = [i.replace("\r", "") for i in mails]
    for msg in mails:
        msg = msg.split('.msg')[0]
        msgFrom, msgSubject = msg.split('_')
        if not str(count) in checkRead.keys():
            # with open('checkRead.json', 'r') as file:
            #     data = json.load(file)
            check = open('checkRead.json', 'w')
            checkRead[count] = False
            json.dump(checkRead, check)
            check.close()
            print(f'{count+1}. (not read) {msgFrom}, {msgSubject}')
            count = count + 1
        elif checkRead[str(count)] == False:
            print(f'{count+1}. (not read) {msgFrom}, {msgSubject}')
            count = count + 1
        elif checkRead[str(count)] == True:
            print(f'{count+1}. {msgFrom}, {msgSubject}')
            count = count + 1

    check.close()
    os.chdir(MYPATH)

def createMailbox(mailboxName):
    myFolders = os.listdir()
    if not mailboxName in myFolders:
        os.mkdir(f'{mailboxName}')
        os.chdir(f'{mailboxName}')
        os.mkdir('Inbox')
        os.mkdir('Project')
        os.mkdir('Important')
        os.mkdir('Work')
        os.mkdir('Spam')
        f = open('numberOfEmails.txt', 'w')
        f.write('0')
        f.close()

    os.chdir(MYPATH)


def readMail(mail2Read, mailboxName, folderOption):
    os.chdir(f'{mailboxName}')
    os.chdir(f'{MailBoxFolders[folderOption]}')
    mails = [i for i in os.listdir() if i.endswith('.msg')]
    if ((mail2Read+1) > len(mails)) or (mail2Read+1) <= 0:
        print("Invalid input.")
        os.chdir(MYPATH)
        return -1
    print(f'Content of email {mail2Read+1}: ')
  
    
    count = 0
    for i in mails:
        if count+1 == mail2Read+1:
            f = open(i)
            print(f.read())
            f.close()
            a = open('checkRead.json', 'r')
            data = json.load(a)
            a.close()
            b = open('checkRead.json', 'w')
            data[count] = True
            json.dump(data, b)
            b.close()

        count = count + 1

    os.chdir(MYPATH)


def getMail():
    configFile = open('config.json')
    configData = json.load(configFile)
    configFile.close()

    HOST = configData["MailServer"]
    PORT = configData["POP3"]

    mailboxName = configData["Username"].split('@')[0]
    # Create mailbox
    if not mailboxName in os.listdir():
        createMailbox(mailboxName)

  

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.recv(1024)
    
        user = f'USER {configData["Username"]}\r\n'
        s.sendall(user.encode())
        s.recv(1024)

        Password = f'PASS {configData["Password"]}\r\n'
        s.sendall(Password.encode())
        s.recv(1024)


        sortEmail(s, mailboxName)

        folderOption = 0
        while True:
            print("\nList of folders in your mailbox: ")
            print("1. Inbox")
            print("2. Project")
            print("3. Important")
            print("4. Work")
            print("5. Spam")
            folderOption = int(input("Which folder to view email: "))
            if folderOption < 1 or folderOption > 5:
                print("Invalid input. Please choose again.")
            else: 
                break


        flag = False
        while True:  
           
            if flag:
                break
            print(f"This is a list of emails in {MailBoxFolders[folderOption]} folder")
            viewEmailFolder(s, mailboxName, folderOption)
            while True:
                mail2Read = input("Which one do you want to read (or press 'enter' to get out, or press '0' to view mail list again): ")
                flag = False
                if mail2Read == '0':
                    break
                    
                elif mail2Read == "":
                    flag = True
                    break
                else:
                    mail2Read = int(mail2Read) - 1
                    readMail(mail2Read, mailboxName ,folderOption)
                

        # s.sendall(b'STAT\r\n')
        # print(s.recv(1024).decode())



        s.sendall(b'QUIT\r\n')
