assets = []
wallets = []
amounts = []
totalAmounts = []
prices = []
LPs = []
LPprices = []
assetsAmount = 0
addressAmount = 0


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
            match self.inPin:
                case self.pin:
                    self.cmd()
                case 0:
                    print("Successfully exited account login")
                case _:
                    print("Wrong pin, please try again")
                    self.loginPin()
        except ValueError:
            print("You did not enter an integer")
            self.loginPin()

    def cmd(self):
        try:
            print(wallets)
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
                    self.cmd()
                case 2:
                    # passing "self" argument as msgSender, to ensure only owner can make changes to OnlyOwner functions
                    try:
                        assets[int(input("Input asset ID\n"))].interact(self.address)
                    except ValueError:
                        print("That asset does not exist")
                    self.cmd()
                case _:
                    print("You did not enter one of the provided options")
                    self.cmd()

        except ValueError:
            print("You did not enter one of the provided options")
            self.cmd()


class asset:
    def __init__(self, addressID):
        # wallets used to find holders
        global wallets
        # assetsAmount used to designate asset ID
        global assetsAmount
        self.name = str(input("Enter name of your new asset\n"))
        self.ticker = str(input("Enter ticker of your new asset\n"))
        self.amount = int(
            input(
                "Enter how many of the new asset should be created? (This will be deposited to your wallet).\n"
            )
        )
        print(addressID)
        self.owner = addressID
        # idk why i want this, i just do
        self.previousOwners = []
        # in case you want multiple admins
        self.admins = []
        # how to add make better?
        # create function to handle holders (not ideal)
        # store assets in wallets (not ideal)
        # how to store wallet address, asset id and asset amount in one?
        # i can only think of adding 2 arrays
        self.holders = []
        self.holderAmounts = []
        for i in range(len(wallets)):
            self.holders.append(wallets[i])
        for i in range(len(self.holders)):
            self.holderAmounts.append(0)
        self.holderAmounts[addressID] += self.amount
        # create ID based on amount of assets before it
        self.id = assetsAmount
        # to ensure each asset has a unique id, i update assetsAmount after each new asset
        assetsAmount += 1
        # approvals will be handled by a multidimensional array
        # approvals[i] will be the wallet
        # approvals[i][j] will be the wallets this wallet has approved
        # approvals[i][j][y] will be the amount approved
        self.approvals = []
        print(f"New asset number = {self.id}\n")

    def interact(self, msgSender):
        self.readData()
        # add more choices
        cmd = int(input("What do you want to do?"))
        match cmd:
            case 1:
                self.transfer(msgSender)
            case 2:
                self.transferOwnership(msgSender)
            case _:
                print("Unknown error")
        self.interact(msgSender)

    def transferOwnership(self, msgSender):
        # make sure caller id is owner
        if msgSender == self.owner:
            global wallets
            try:
                self.newOwner = wallets[
                    int(input("What wallet should be the new owner?\n"))
                ]
                self.cmd = input(
                    f"Are you sure you want to change owner of {self.name} ({self.ticker}) from {self.owner} to {self.newOwner}? (Yes = True/No = False)\n"
                )
                match self.cmd:
                    case True:
                        # to record all previous owners
                        self.previousOwners.append(self.owner)
                        self.owner = self.newOwner
                    case False:
                        print("Answered no, going back to interaction menu")
                        # return back to interact function
                        self.interact(self, msgSender)
                    case _:
                        print("Command was not true or false")
            except IndexError:
                print("Could not find wallet")
            except ValueError:
                print("Please input a whole number")
            finally:
                print("Unknown error when finding new owner wallet number")

        else:
            print("You are not the owner of this asset")

    def mint(self):
        print(f"Current amount is of asset number {self.id} is {self.amount}\n")
        self.amount = int(input(f"How many of {self.name} do you want to create?\n"))

    def readData(self):
        self.updateWallets()
        print(
            f"""
        Name: {self.name}\n")
        Ticker: {self.ticker}
        Amount: {self.amount}\n
        Holders:
        """
        )
        for i in range(len(self.holders)):
            print(
                f"Holder {self.holders[i].address} with {self.holderAmounts[i]} {self.name}"
            )

    def transfer(self, msgSender):
        cmd = int(
            input(
                f"""What do you want to do with wallet {msgSender}'s '{self.name}, ({self.ticker})'?\n 
    This wallet holds {self.holderAmounts[msgSender]} {self.ticker}.\n"""
            )
        )
        match cmd:
            case 1:
                transferAmount = int(input("how much do you want to transfer?"))
                receiver = int(input("what wallet do you want to transfer to?"))
                self.holderAmounts[msgSender] -= transferAmount
                self.holderAmounts[receiver] += transferAmount

    def approve(self, msgSender):
        global wallets
        # unorderly
        # structs or mappings (like in Solidity) would come in handy
        # let wallet approve other wallet to transfer assets
        # example: wallet 1 allows wallet 2 to transfer 1 unit
        # in solidity, this is done by a mapping an address to an asset, then mapping that to a number
        approval = int(input("What wallet do you want to approve?"))
        amount = int(input("How much do you want to approve this for?"))

    def updateWallets(self):
        global wallets
        if len(self.holders) != len(wallets):
            print("updating wallets")
            for i in range(len(wallets)):
                try:
                    self.holders[i]
                except IndexError:
                    self.holders.append(wallets[i])
        if len(self.holderAmounts) != len(wallets):
            # if not all wallets are accounted for in holderAmounts var
            print("updating wallets")
            for i in range(len(self.holders)):
                # if self.holderAmounts[i] exists, don't do anything
                # with error "IndexError", add a new index to holdersAmount
                # not ideal, creates more holders than there are wallets. when wallet created, it keeps assets
                # plans forward: if trying to send assets to non-existing holder number, create holder number
                try:
                    self.holderAmounts[i]
                except IndexError:
                    self.holderAmounts.append(0)


class LP:
    def __init__(self, asset1ID, asset2ID):
        # give 2 assets
        #   asset ID
        #   asset amount?
        # this will be used for trading 2 assets in what is known as a "liquidity pool"
        # search it up for more
        # https://www.youtube.com/watch?v=dVJzcFDo498&

        pass


def main():
    while True:
        try:
            # inoptimal?
            # not sure about performance specs
            # try to find better way
            cmd = int(
                input(
                    "What do you want to do?\n 1. Create new wallet\n 2. Use existing wallet\n"
                )
            )
            match cmd:
                case 1:
                    wallets.append(wallet())
                    print(wallets)
                case 2:
                    try:
                        cmd = int(input("What wallet do you want to use?\n"))
                        try:
                            wallets[cmd].login()
                        except IndexError:
                            print(f"Wallet number {cmd} does not exist")
                        finally:
                            pass
                    except ValueError:
                        print("Please input a whole number")
                    finally:
                        pass
                case _:
                    print("Please enter one of the provided options")
        except ValueError:
            print("Please enter one of the provided options (ERROR CODE: ValueError)")
        finally:
            print("Fatal error. Returning to start.")


main()
