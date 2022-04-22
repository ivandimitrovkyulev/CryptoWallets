import json

from common.helpers import print_last_transactions


no_of_txns = int(input("Enter how many transactions to print?: "))

filename = input("Enter name of .json file containing addresses to query: ")

with open(filename, 'r') as json_file:
    address_dict = json.load(json_file)

    print(f"Last {no_of_txns} transactions:")
    # Infinite scraping. Keyboard interrupt to stop.
    print_last_transactions(address_dict, no_of_txns)
