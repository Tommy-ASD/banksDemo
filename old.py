accounts = []
takenNames = []


class account:
    def __init__(self):
        self.balance = 0
        self.TXNhist = []
        self.activated = False
        self.newPin = 0
        self.pinConf = 0
        self.pin = 0
        self.inPin = 0
        self.nameAssigned = False
        self.name = "Unnamed"
        self.name4sale = []
        global accNrIn

    def login(self):
        if self.activated == False:
            self.createPin()
        else:
            self.loginPin()

    def createPin(self):
        print(
            "Please choose a pin code for this account. The pin should be between 4 and 8 digits. If you no longer wish to choose this account, input the number 0"
        )
        self.newPin = int(input())
        if len(str(self.newPin)) >= 4 and len(str(self.newPin)) <= 8:
            print("Please confirm your pin")
            self.pinConf = int(input())
            if self.newPin == self.pinConf:
                self.pin = self.newPin
                print("Pin successfully created!")
                self.activated = True
                self.cmd()

            else:
                print("Your 2 pin codes did not match, please try again.")
                self.createPin()
        elif self.newPin == 0:
            print("Successfully exited pin code creation")
        else:
            print("Pin should be between 4 and 8 numbers long")
            self.createPin()

    def loginPin(self):
        print(
            "Please enter your Pin code. If you wish to change accounts, enter the number 0."
        )
        self.inPin = int(input())
        if self.inPin == self.pin:
            self.cmd()
        elif self.inPin == 0:
            print("Successfully exited account login")
        else:
            print("Wrong pin, please try again")
            self.loginPin()

    def cmd(self):
        if self.nameAssigned == True:
            print("Welcome back, " + self.name + "! Happy to see you!")
        print("Current account balance is " + str(self.balance))
        func = int(
            input(
                """What would you like to do with this account?
    1: Deposit
    2: Withdraw
    3: Transfer between accounts
    4: See balance and transaction history
    5: Name/rename your account
    6: Log out of your account
            """
            )
        )
        if func == 1:
            self.deposit()
        elif func == 2:
            self.withdraw()
        elif func == 3:
            self.transfer()
        elif func == 4:
            self.info()
        elif func == 5:
            self.nameFunc()
        elif func == 6:
            print("Successfully logged out")

    def deposit(self):
        amount = float(input("Enter amount to be deposited: "))
        self.balance += amount
        print("Amount Deposited:", amount)
        self.TXNhist.append(
            "Deposited " + str(amount) + ", balance is " + str(self.balance) + "."
        )
        self.cmd()

    def withdraw(self):
        amount = float(input("Enter amount to be withdrawn: "))
        if self.balance >= amount:
            self.balance -= amount
            self.TXNhist.append(
                "Withdrew " + str(amount) + ", balance is " + str(self.balance) + "."
            )
            print("You Withdrew:", amount)
        else:
            print("Insufficient balance")
        self.cmd()

    def transfer(self):
        amount = float(input("Enter amount to be transferred: "))
        if self.balance >= amount:
            reci = int(input("Enter recipient account number: "))
            # This is because the array starts at value 0, while the length of the array starts at 1, this is for correction
            reciOut = reci - 1
            if reci <= 0:
                print("Sorry, account numbers cannot be lower than zero")
            elif reci >= (len(accounts) + 1):
                print("Sorry, that account does not exist yet")
            else:
                self.balance -= amount
                accounts[reciOut].balance += amount
                self.TXNhist.append(
                    "Transferred "
                    + str(amount)
                    + " to account number "
                    + str(reci)
                    + ", balance is "
                    + str(self.balance)
                    + "."
                )
                accounts[reciOut].TXNhist.append(
                    "Received "
                    + str(amount)
                    + " from account number "
                    + str(accNrIn)
                    + ", balance is "
                    + str(accounts[reciOut].balance)
                    + "."
                )
                print(
                    "You transferred: "
                    + str(amount)
                    + " to account number "
                    + str(reci)
                )
        else:
            print("Insufficient balance")
        self.cmd()

    def info(self):
        print("Transaction history: ", self.TXNhist)
        print("Current balance:", self.balance)
        self.cmd()

    def nameFunc(self):
        global takenNames
        if self.nameAssigned == False:
            print("What would you like to name your account?")
            self.newName = str(input())
            if self.newName in takenNames:
                print("That name is taken, try another one")
            else:
                self.name = self.newName
                self.nameAssigned = True
        else:
            self.nameCMD = int(
                input(
                    'This account has already been named "'
                    + self.name
                    + """", would you like to rename it?
            1: Yes
            2: No
            3: Remove account name
            """
                )
            )
            if self.nameCMD == 1:
                print(
                    "You are currently renaming your account. What should the new name be?"
                )
                self.newName = str(input())
                if self.newName == self.name:
                    print("That is your current name")
                elif self.newName in takenNames:
                    print("That name is taken, try another one")
                else:
                    self.name = self.newName
            elif self.nameCMD == 2:
                print("Returning to main page")
            elif self.nameCMD == 3:
                self.name = "Unnamed"
                self.nameAssigned = False
                print("Account name successfully deleted")

                # WIP
        #            elif self.nameCMD == 4:
        #                self.nameSale = int(input('How much would you like to sell your name for? Enter 0 if you do not want to sell your name.')
        #                if self.nameSale == 0:
        #                    print('Name sale cancelled')
        #                else:
        #                    self.name4sale.append(self.name)
        #                    self.name = 'Unnamed'
        #                    self.nameAssigned = False

        self.cmd()


print(
    """Hello, and welcome to "A Bank With A Very Creative Name"!
First order of business; Account creation. Account number 1 was just created."""
)
accounts.append(account())
# Account creation and login
while True:
    # Taken names are deleted, as they are immediately replaced
    takenNames = []
    for i in range(len(accounts)):
        y = i - 1
        takenNames.insert(y, accounts[y].name)
    cmd = int(
        input(
            """What would you like to?
    1: Add new account
    2: View the names of accounts
    3: Log in to an existing account
    """
        )
    )
    if cmd == 1:
        print("Successfully created account number " + str(len(accounts) + 1))
        accounts.append(account())
    elif cmd == 2:
        for i in range(len(accounts)):
            if accounts[i].name == "Unnamed":
                print(
                    "Account number "
                    + str(i + 1)
                    + " is unnamed, with a balance of "
                    + str(accounts[i].balance)
                )
            else:
                print(
                    "Account number "
                    + str(i + 1)
                    + " is named "
                    + accounts[i].name
                    + ", with a balance of "
                    + str(accounts[i].balance)
                )
    elif cmd == 3:
        print("What account would you like to interact with?")
        accNrIn = int(input())
        accNr = accNrIn - 1
        if (accNr + 1) > len(accounts):
            print("Sorry, that account does not exist yet.")
        elif accNr < 0:
            print("Sorry, account numbers cannot be lower than zero")
        else:
            accounts[accNr].login()
    else:
        print("Invalid input")
