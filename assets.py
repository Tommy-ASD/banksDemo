from vars import wallets, assetsAmount


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
        print(f"Address ID: {addressID}")
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
        self.interact(addressID)

    def interact(self, msgSender):
        self.readData()
        # add more choices
        self.transfer(msgSender)
        self.transferOwnership(msgSender)

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
                try:
                    if self.cmd:
                        # to record all previous owners
                        self.previousOwners.append(self.owner)
                        self.owner = self.newOwner
                    else:
                        print("Answered no, going back to interaction menu")
                        # return back to interact function
                        self.interact(self, msgSender)
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
                transferAmount = int(input("how much do you want to transfer?\n"))
                receiver = int(input("what wallet do you want to transfer to?\n"))
                # idkf what's going on here but it doesn't work
                try:
                    self.holderAmounts[msgSender] -= transferAmount
                    self.holderAmounts[receiver] += transferAmount
                except ValueError:
                    print(f"Wallet number {receiver} does not exist")

    def approve(self, msgSender):
        global wallets
        # unorderly
        # structs or mappings (like in Solidity) would come in handy
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
