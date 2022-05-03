"""
Main script that screens specified blockchain wallets and notifies when a new transaction occurs.
Creates a multiprocessing pool of wallet addresses to scrape.
To run:
var="$(cat wallets.json)"
python3 main.py "$var"
"""
import os
import sys
import json
from atexit import register
from datetime import datetime

from src.common.exceptions import exit_handler
from src.common.variables import time_format
from src.multi_process.scrape import scrape_wallets_multiprocess


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

    print(f"{timestamp} - {program_name}\n"
          f"Started screening the following addresses:\n"
          f"{addresses}")

    # Infinite scraping. Keyboard interrupt to stop.
    scrape_wallets_multiprocess(address_dict)
    
else:
    print("Please provide only one argument of type string.")
    sys.exit()
