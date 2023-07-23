from utils.web3Utils import Web3Utils
from utils import str_to_file


def list_to_file(file_name: str, wallets: list):
    str_to_file(file_name, '\n'.join([wallet[1] for wallet in wallets]))


def generate_random_wallets(amount: int = 100):
    wallets = []
    for _ in range(amount):
        w3 = Web3Utils()
        w3.create_wallet()
        wallets.append((w3.acct.address, w3.acct.key.hex()))
    list_to_file('data\\inputs\\wallets_backup.txt', wallets)
    return wallets
