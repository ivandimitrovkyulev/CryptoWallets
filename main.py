import sys
import json
from datetime import datetime
from common.helpers import scrape_multiple_wallets
from common.variables import time_format


timestamp = datetime.now().astimezone().strftime(time_format)

if len(sys.argv) < 2:
    print("Please provide a string of addresses as an argument to process.\n"
          "For example, given a 'wallets.json' file, provide var, where var='$(cat wallets.json)'")
    sys.exit()
elif len(sys.argv) == 2:
    text = sys.argv[-1]
    address_dict = json.loads(text)

    # Print to terminal
    addresses = ""
    for index, address in enumerate(address_dict):
        wallet_name = address_dict[address]['name']
        addresses += f"{index + 1}. {address}, {wallet_name}\n"

    print(f"{timestamp}\nStarted screening the following addresses: \n{addresses}")

    # Infinite scraping. Keyboard interrupt to stop.
    scrape_multiple_wallets(address_dict)
else:
    print("Please provide only one argument of type string.")
    sys.exit()
