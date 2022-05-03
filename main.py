"""
Main script that screens specified blockchain wallets and notifies when a new transaction occurs.

Save addresses in a variable:
var="$(cat wallets.json)"

To creates a multiprocessing pool of wallet addresses to scrape:
python3 main.py -m "$var"

To creates a subprocess with Popen for each wallet address to scrape:
python3 main.py -s "$var"
"""
import os
import sys
import json
from atexit import register
from datetime import datetime

from src.common.exceptions import exit_handler
from src.common.variables import time_format

from src.multi_process.scrape import scrape_wallets_multiprocess
from src.sub_process.scrape import scrape_wallets_subprocess


timestamp = datetime.now().astimezone().strftime(time_format)
program_name = os.path.basename(__file__)

# Register function to be executed when script terminates
register(exit_handler, program_name)


if len(sys.argv) != 3:
    print("Please provide scrape type and a string of addresses as an argument to process.\n"
          "For example, given a 'wallets.json' file, provide '$var', where var='$(cat wallets.json)'")
    sys.exit()

else:
    # Read input string and convert it to a dictionary
    address_dict = json.loads(sys.argv[-1])

    # Print to terminal
    addresses = ""
    for index, address in enumerate(address_dict):
        wallet_name = address_dict[address]['name']
        addresses += f"{index + 1}. {address}, {wallet_name}\n"

    address_message = f"Started screening the following addresses:\n"\
                      f"{addresses}"

    if sys.argv[1] == "-m":
        message = f"{timestamp} - {program_name} - multiprocessing has started\n"
        print(message + address_message)
        # Infinite scraping. Keyboard interrupt to stop.
        scrape_wallets_multiprocess(address_dict)

    elif sys.argv[1] == "-s":
        message = f"{timestamp} - {program_name} - subprocessing has started\n"
        print(message + address_message)
        # Infinite scraping. Keyboard interrupt to stop.
        scrape_wallets_subprocess(address_dict)
