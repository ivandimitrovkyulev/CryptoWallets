from re import split
from datetime import datetime
from common.helpers import scrape_multiple_wallets
from common.variables import time_format


timestamp = datetime.now().astimezone().strftime(time_format)

# Get input from script
with open('addresses.txt', 'r') as file:
    address_list = [adr.split("\n")[0] for adr in file.readlines() if adr != "\n"]

addresses = ""
for index, address in enumerate(address_list):
    addresses += f"{index + 1}. {address}\n"

print(f"{timestamp}\nStarted screening the following addresses: \n{addresses}")

# Infinite scraping. Keyboard interrupt to stop.
scrape_multiple_wallets(address_list)
