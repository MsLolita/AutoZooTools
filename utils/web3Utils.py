from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3


class Web3Utils:
    def __init__(self, http_provider: str = 'https://http-mainnet.cube.network', mnemonic: str = None, key: str = None):
        self.w3 = Web3(Web3.HTTPProvider(http_provider))
        Account.enable_unaudited_hdwallet_features()
        if mnemonic:
            self.mnemonic = mnemonic
            self.acct = Account.from_mnemonic(mnemonic)
        elif key:
            self.mnemonic = ""
            self.acct = Account.from_key(key)

    def create_wallet(self):
        self.acct, self.mnemonic = Account.create_with_mnemonic()
        return self.acct, self.mnemonic

    def sign(self, msg: str):
        return self.w3.eth.account.sign_message(encode_defunct(
            text=msg
        ), self.acct.key)

    def get_signed_code(self, msg) -> str:
        return self.sign(msg).signature.hex()
