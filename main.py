from threading import Thread
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

from common.helpers import scrape_wallet
from common.variables import (
    CHROME_LOCATION,
    address_list,
)


"""
for address in address_list:
    print(address)
    Thread(target=scrape_wallet, args=(address,)).start()"""

address = address_list[0]
scrape_wallet(address)
