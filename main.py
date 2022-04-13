from re import split
from datetime import datetime
from common.helpers import scrape_multiple_wallets
from common.variables import time_format


timestamp = datetime.now().astimezone().strftime(time_format)

# Get input from script
script_input = input("Enter addresses to screen: ")

address_list = []
for word in split("[\s,]+", script_input):
    address_list.append(word)

addresses = ""
for index, address in enumerate(address_list):
    addresses += f"{index + 1}. {address}\n"

print(f"{timestamp}\nStarted screening the following addresses: \n{addresses}")

# Infinite scraping. Keyboard interrupt to stop.
scrape_multiple_wallets(address_list)
