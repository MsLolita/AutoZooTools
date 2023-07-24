import requests
import pyuseragents

from anticaptchaofficial.turnstileproxyless import turnstileProxyless

from data.captcha import ANTICAPTCHA_API_KEY, SITE_KEY, URL
from utils import str_to_file, logger


class ZooTools:
    event_id = None
    referral = None

    def __init__(self, email: str, address: str, proxy: str = None):
        self.email = email
        self.address = address
        self.proxy = f"http://{proxy}" if proxy else None

        self.headers = {
            'authority': 'audience-consumer-api.zootools.co',
            'accept': '*/*',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer',
            'content-type': 'application/json',
            'origin': 'https://form.zootools.co',
            'user-agent': pyuseragents.random()
        }

        self.session = requests.Session()

        self.session.headers.update(self.headers)
        self.session.proxies.update({'https': self.proxy, 'http': self.proxy})

    def enter_raffle(self):
        url = f'https://audience-consumer-api.zootools.co/v3/lists/{ZooTools.event_id}/members'

        json_data = {
            'utmSource': '',
            'utmMedium': '',
            'utmCampaign': '',
            'utmTerm': '',
            'utmContent': '',
            'pageReferrer': '',
            'email': self.email,
            'cryptoAddress': self.address,
            'hiddenFields': {
                'productId': '',
                'projectId': '',
                'teamId': '',
                'userId': '',
            },
            'captchaToken': ZooTools.__bypass_turnstile_captcha(),
            'referral': ZooTools.referral,
        }

        response = self.session.post(url, json=json_data)

        return response.ok, response.text

    def logs(self):
        file_msg = f"{self.email}|{self.address}|{self.proxy}"
        str_to_file(f"data\\logs\\success.txt", file_msg)
        logger.success(f"Register {self.email}")

    def logs_fail(self, msg: str = ""):
        file_msg = f"{self.email}|{self.address}|{self.proxy}"
        str_to_file(f"data\\logs\\failed.txt", file_msg)
        logger.error(f"Failed {self.email} {msg}")

    @staticmethod
    def __bypass_turnstile_captcha():
        solver = turnstileProxyless()
        solver.set_key(ANTICAPTCHA_API_KEY)
        solver.set_website_url(URL)
        solver.set_website_key(SITE_KEY)

        solver.set_action("login")
        # solver.set_soft_id(0)
        token = solver.solve_and_return_solution()

        if not token:
            logger.error("Failed to solve captcha! Please put your API key in data/captcha/__init__.py")
            exit()

        return token
