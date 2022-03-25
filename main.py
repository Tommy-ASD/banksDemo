from multiprocessing.sharedctypes import Value


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
            assets.append(asset(self.address))
        elif cmd == 2:
            # passing "self" argument as callerID, to ensure only owner can make changes to OnlyOwner functions
            assets[int(input("Input asset ID\n"))].interact(self.address)
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
        print(f"New asset number = {self.id}\n")

    def interact(self, callerID):
        self.readData()
        # add more choices
        self.updateWallets()
        self.changeHolders(callerID)
        self.changeOwner(callerID)

    def changeOwner(self, callerID):
        # make sure caller id is owner
        if callerID == self.owner:
            global wallets
            try:
                self.newOwner = wallets[
                    int(input("What wallet should be the new owner?\n"))
                ]
                self.cmd = input(
                    f"Are you sure you want to change owner of {self.name} ({self.ticker}) from {self.owner} to {self.newOwner}? (Yes = True/No = False)\n"
                )
                try:
                    if self.cmd:
                        # to record all previous owners
                        self.previousOwners.append(self.owner)
                        self.owner = self.newOwner
                    else:
                        print("Answered no, going back to interaction menu")
                        # return back to interact function
                        self.interact(self, callerID)
                except ValueError:
                    print("Please only input one of the provided option")
            except IndexError:
                print("Could not find wallet")
            except ValueError:
                print("Please input a whole number")
            finally:
                print("Unknown error when finding new owner wallet number")

        else:
            print("You are not the owner of this asset")

    def createMore(self):
        print(f"Current amount is of asset number {self.id} is {self.amount}\n")
        self.amount = int(input(f"How many of {self.name} do you want to create?\n"))

    def readData(self):
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

    def changeHolders(self, callerID):
        cmd = int(
            input(
                f"""What do you want to do with wallet {callerID}'s '{self.name}, ({self.ticker})'?\n 
    This wallet holds {self.holderAmounts[callerID]} {self.ticker}.\n"""
            )
        )
        match cmd:
            case 1:
                transferAmount = int(input("how much do you want to transfer?"))
                transferredTo = int(input("what wallet do you want to transfer to?"))
                self.holderAmounts[callerID] -= transferAmount
                self.holderAmounts[transferredTo] += transferAmount

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
            if cmd == 1:
                wallets.append(wallet())
                print(wallets)
            elif cmd == 2:
                try:
                    cmd = int(input("What wallet do you want to use?\n"))
                    try:
                        wallets[cmd].interact()
                    except IndexError:
                        print(f"Wallet number {cmd} does not exist")
                    finally:
                        print("Unknown error, please try again")
                except ValueError:
                    print("Please input a whole number")
                finally:
                    print("Unknown error, please try again")
            else:
                print("Please enter one of the provided options")
        except ValueError:
            print("Please enter one of the provided options")


main()
