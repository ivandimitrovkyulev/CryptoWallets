import json
import os

from multiprocessing.dummy import Pool
from src.common.driver import chrome_driver
from src.multi_process.scrape import get_last_txns


def print_last_txns(
        addr_dict: dict,
        no_txns: int = 3,
) -> None:
    """
    Prints the last number of transactions for the specified addresses.

    :param addr_dict: Dictionary of addresses
    :param no_txns: No. of transactions to query and print
    :returns: None
    """

    # construct url and open webpage
    tab_names = []
    wallet_names = []
    for address in addr_dict:
        chrome_driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_names.append(chrome_driver.window_handles[-1])
        wallet_names.append(address_dict[address]['name'])

    args = [(tab, wallet, no_txns) for tab, wallet in zip(tab_names, wallet_names)]

    with Pool(os.cpu_count()) as pool:
        batch = pool.starmap(get_last_txns, args)

        for transactions, address in zip(batch, addr_dict):

            print(f"Address: {address}, {addr_dict[address]['name']}")
            for info in transactions:
                txn_details = transactions[info]
                print(txn_details)

            print()

    # Quit chrome driver
    chrome_driver.quit()


no_of_txns = int(input("Enter how many transactions to print?: "))

filename = input("Enter name of .json file containing addresses to query: ")

with open(filename, 'r') as json_file:
    address_dict = json.load(json_file)

    print(f"Last {no_of_txns} transactions:")
    # Infinite scraping. Keyboard interrupt to stop.
    print_last_txns(address_dict, no_of_txns)
