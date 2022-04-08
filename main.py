from common.helpers import scrape_wallets
from common.variables import address_list
from datetime import datetime


timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
addresses = ""
for address in address_list:
    addresses += address + "\n"

print(f"{timestamp} - Started scraping DeBank for the following addresses: \n{addresses}")
# Infinite scraping. Keyboard interrupt to stop.
scrape_wallets(address_list)
