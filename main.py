import sys
from datetime import datetime
from common.helpers import scrape_multiple_wallets
from common.variables import time_format


timestamp = datetime.now().astimezone().strftime(time_format)

if len(sys.argv) < 2:
    print("Please provide a string of addresses to process. For example a file named addresses.txt,\n"
          "that has only one address per line, provide var, where var=$(cat addresses.txt)")
    sys.exit()
elif len(sys.argv) == 2:
    text = sys.argv[-1]
    # Get input from script
    address_list = [line for line in text.split("\n") if line != "\n"]

    addresses = ""
    for index, address in enumerate(address_list):
        addresses += f"{index + 1}. {address}\n"

    print(f"{timestamp}\nStarted screening the following addresses: \n{addresses}")

    # Infinite scraping. Keyboard interrupt to stop.
    scrape_multiple_wallets(address_list)
else:
    print("Please provide only one argument.")
    sys.exit()
