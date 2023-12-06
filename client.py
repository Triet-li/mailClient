import getMail
import sendMail


while True:
    print("Menu: ")
    print("1. To send email")
    print("2. To view received emails")
    print("3. To exit")
    option = int(input("Picking: "))
    if option == 3:
        break
    elif option == 2:
        sendMail.sendMail()
    elif option == 1:
        getMail.getMail()
    else:
        print("Invalid input. Please choose again.")
