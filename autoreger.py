from concurrent.futures import ThreadPoolExecutor

from utils import shift_file, logger
from utils.auto_generate.emails import generate_random_emails
from utils.auto_generate.wallets import generate_random_wallets
from utils.file_to_list import file_to_list
from zootools import ZooTools


class AutoReger:
    def __init__(self):
        self.emails_path: str = "data\\inputs\\emails.txt"
        self.proxies_path: str = "data\\inputs\\proxies.txt"
        self.wallets_path: str = "data\\inputs\\wallets.txt"

        self.success = 0

    def get_accounts(self):
        emails = file_to_list(self.emails_path)
        wallets = file_to_list(self.wallets_path)
        proxies = file_to_list(self.proxies_path)

        if not emails:
            logger.info(f"Generated random emails!")
            emails = generate_random_emails(5)

        if not wallets:
            logger.info(f"Generated random wallets!")
            wallets = [wallet[0] for wallet in generate_random_wallets(len(emails))]

        accounts = []

        if len(emails) < len(wallets):
            for i in range(len(emails)):
                accounts.append((emails[i], wallets[i], proxies[i] if proxies else None))
        else:
            for i in range(len(wallets)):
                accounts.append((emails[i], wallets[i], proxies[i] if proxies else None))

        return accounts

    def remove_account(self):
        return shift_file(self.emails_path), shift_file(self.wallets_path), shift_file(self.proxies_path)

    def start(self):
        referral_link = input("Referral link(https://form.zootools.co/go/bLFJhrGfkOoEQgt3I3LR?ref=oshDiqOc2PLuLpexCzll): ")

        ZooTools.event_id = referral_link.split('/')[-1].split('?')[0]
        ZooTools.referral = referral_link.split('?ref=')[-1]

        threads = int(input("Enter amount of threads: "))

        accounts = self.get_accounts()
        print(accounts)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.register, accounts)

        if self.success:
            logger.success(f"Successfully registered {self.success} accounts :)")
        else:
            logger.warning(f"No accounts registered :(")

    def register(self, account: tuple):
        zoo_tools = ZooTools(*account)
        is_ok = False

        try:
            is_ok = zoo_tools.enter_raffle()
        except Exception as e:
            logger.error(f"Error {e}")

        self.remove_account()

        if is_ok:
            zoo_tools.logs()
            self.success += 1
        else:
            zoo_tools.logs_fail()

    def check_files_empty(self):
        # check if emails in not empty
        if AutoReger.is_file_empty(self.emails_path):
            logger.warning(f"No emails in path {self.emails_path}!")
            return

        # check if proxies in not empty
        if AutoReger.is_file_empty(self.wallets_path):
            logger.warning(f"No wallets in path {self.wallets_path}!")
            return

        logger.info(f"Starting registration accounts...")

    @staticmethod
    def is_file_empty(path: str):
        return not open(path).read().strip()
