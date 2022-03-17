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

    def interact(self):
        print(wallets)
        cmd = int(
            input("What do you want to do?\n 1. Create asset\n 2. Change asset stats\n")
        )
        if cmd == 1:
            # pass self.address in as owner
            assets.append(asset(self))
        elif cmd == 2:
            # passing "self" argument as callerID, to ensure only owner can make changes to OnlyOwner functions
            assets[int(input("Input asset ID\n"))].interact(self)
        elif cmd == 3:
            pass


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
        self.owner = addressID
        # idk why i want this, i just do
        self.previousOwners = []
        # in case you want multiple admins
        self.admins = []
        self.holders = [addressID]
        self.holdersAmounts = [self.amount]
        # create ID based on amount of assets before it
        self.id = assetsAmount
        # to ensure each asset has a unique id, i update assetsAmount after each new asset
        assetsAmount += 1
        print(f"New asset number = {self.id}\n")

    def interact(self, callerID):
        self.readData()
        # add more choices
        self.changeOwner(callerID)

    def changeOwner(self, callerID):
        # make sure caller id is owner
        if callerID == self.owner:
            global wallets
            self.newOwner = wallets[
                int(input("What wallet should be the new owner?\n"))
            ]
            self.cmd = input(
                f"Are you sure you want to change owner of {self.name} ({self.ticker}) from {self.owner} to {self.newOwner}? (Yes = True/No = False)\n"
            )
            if self.cmd:
                # to record all previous owners
                self.previousOwners.append(self.owner)
                self.owner = self.newOwner
            else:
                print("Answered no, going back to interaction menu")
                # return back to interact function
                self.interact(self, callerID)

        else:
            print("You are not the owner of this asset")

    def createMore(self):
        print(f"Current amount is of asset number {self.id} is {self.amount}\n")
        self.amount = int(input(f"How many of {self.name} do you want to create?\n"))

    def readData(self):
        print(f"Name: {self.name}\n")
        print(f"Ticker: {self.ticker}\n")
        print(f"Amount: {self.amount}\n")


class LP:
    def __init__(self):
        # give 2 assets
        # this will be used for trading 2 assets in what is known as a "liquidity pool"
        # search it up for more

        pass


def main():
    while True:
        cmd = int(
            input(
                "What do you want to do?\n 1. Create new wallet\n 2. Use existing wallet\n"
            )
        )
        if cmd == 1:
            wallets.append(wallet())
            print(wallets)
        elif cmd == 2:
            cmd = int(input("What wallet do you want to use?\n"))
            wallets[cmd].interact()


main()
