from wallets import wallet
from vars import wallets


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
                        wallets[cmd].login()
                    except IndexError:
                        print(f"Wallet number {cmd} does not exist")
                    finally:
                        pass
                except ValueError:
                    print("Please input a whole number")
                finally:
                    pass
            else:
                print("Please enter one of the provided options")
        except ValueError:
            print("Please enter one of the provided options")


main()
