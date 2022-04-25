import os
import sys
import json
from atexit import register
from datetime import datetime

from common.scrape import scrape_multiple_wallets
from common.exceptions import exit_handler
from common.variables import time_format


timestamp = datetime.now().astimezone().strftime(time_format)
program_name = os.path.basename(__file__)

# Register function to be executed when script terminates
register(exit_handler, program_name)

if len(sys.argv) < 2:
    print("Please provide a string of addresses as an argument to process.\n"
          "For example, given a 'wallets.json' file, provide var, where var='$(cat wallets.json)'")
    sys.exit()
elif len(sys.argv) == 2:
    # Read input string and convert it to a dictionary
    address_dict = json.loads(sys.argv[-1])

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
