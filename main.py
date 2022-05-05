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
from datetime import datetime

from src.common.variables import time_format


timestamp = datetime.now().astimezone().strftime(time_format)
program_name = os.path.basename(__file__)


if "-h" in sys.argv or "--help" in sys.argv:
    print(f"Usage: python3 {program_name} [MODE] [ADDRESSES]\n"
          f"MODE: -s for subprocessing, -m for multiprocessing\n"
          f"ADDRESSES: A .json file with addresses. Store at var='$(cat wallets.json)' and pass '$var'")
    sys.exit()

if len(sys.argv) != 3:
    print("Please provide Scrape Type and String of Addresses as an argument to process.\n"
          "For example, given a 'wallets.json' file, provide '$var', where var='$(cat wallets.json)'")
    sys.exit()

else:
    # Import module
    from atexit import register

    from src.common.exceptions import exit_handler
    from src.common.driver.driver import chrome_driver

    # Register function to be executed when script terminates
    register(exit_handler, chrome_driver, program_name)

    # Read input string and convert it to a dictionary
    address_dict = json.loads(sys.argv[-1])

    # Print to terminal
    addresses = ""
    for index, address in enumerate(address_dict):
        wallet_name = address_dict[address]['name']
        addresses += f"{index + 1}. {address}, {wallet_name}\n"

    address_message = f"Started screening the following addresses:\n"\
                      f"{addresses}"

    if sys.argv[1].lower() == "-m":
        # Import module
        from src.multi_process.scrape import scrape_wallets_multiprocess

        message = f"{timestamp} - {program_name} - multiprocessing has started\n"
        print(message + address_message)
        # Infinite scraping. Keyboard interrupt to stop.
        scrape_wallets_multiprocess(address_dict)

    elif sys.argv[1].lower() == "-s":
        # Import module
        from src.sub_process.scrape import scrape_wallets_subprocess

        message = f"{timestamp} - {program_name} - subprocessing has started\n"
        print(message + address_message)
        # Infinite scraping. Keyboard interrupt to stop.
        scrape_wallets_subprocess(address_dict)
