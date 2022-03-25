from vars import assets, addressAmount
from assets import asset


class wallet:
    def __init__(self):
        global addressAmount
        self.address = addressAmount
        addressAmount += 1
        print("created wallet")
        self.pin = None
        self.newPin = int
        self.activated = False

    def login(self):
        if self.activated:
            self.loginPin()
        else:
            self.createPin()

    def createPin(self):
        print(
            "Please choose a pin code for this account. The pin should be between 4 and 8 digits. If you no longer wish to choose this account, enter the number 0"
        )
        try:
            self.newPin = int(input())
            if len(str(self.newPin)) >= 4 and len(str(self.newPin)) <= 8:
                print("Please confirm your pin")
                self.pinConf = int(input())
                match self.newPin:
                    case self.pinConf:
                        self.pin = self.newPin
                        print("Pin successfully created!")
                        self.activated = True
                        self.cmd()
                    case 0:
                        pass
                    case _:
                        print("Please input the same number")
                        self.createPin()
            else:
                print("Not within 4 and 8 integers")
                self.createPin()
        except ValueError:
            print("You did not enter an integer")
            self.createPin()

    def loginPin(self):
        print(
            "Please enter your Pin code. If you no longer wish to log into this account, enter the number 0."
        )
        try:
            self.inPin = int(input())
            if self.inPin == self.pin:
                self.cmd()
            elif self.inPin == 0:
                print("Successfully exited account login")
            else:
                print("Wrong pin, please try again")
                self.loginPin()
        except ValueError:
            print("You did not enter an integer")
            self.loginPin()

    def cmd(self):
        try:
            cmd = int(
                input(
                    "What do you want to do?\n 1. Create asset\n 2. Change asset stats\nEnter 0 to log out\n"
                )
            )
            match cmd:
                case 0:
                    pass
                case 1:
                    # pass self.address in as owner
                    assets.append(asset(self.address))
                case 2:
                    # passing "self" argument as msgSender, to ensure only owner can make changes to OnlyOwner functions
                    assets[int(input("Input asset ID\n"))].interact(self.address)
                case _:
                    print("You did not enter one of the provided options")
                    self.cmd()

        except ValueError:
            print("You did not enter one of the provided options")
            self.cmd()
