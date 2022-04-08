from common.helpers import scrape_wallets
from common.variables import address_list
from datetime import datetime


timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
addresses = ""
for index, address in enumerate(address_list):
    addresses += f"{index + 1}. {address}\n"

print(f"{timestamp}\nStarted screening the following addresses: \n{addresses}")
# Infinite scraping. Keyboard interrupt to stop.
scrape_wallets(address_list)
