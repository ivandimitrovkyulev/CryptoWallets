import json
from lxml import html

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.common.driver.driver import chrome_driver
from src.common.page import scrape_table
from src.common.variables import (
    table_element_name,
    table_element_id,
)


def get_last_txns(
        driver: Chrome,
        tab_name: str,
        element_name: str,
        element_id: str,
        no_of_txns: int,
        max_wait_time: int,
) -> dict:
    """
    Searches DeBank for an Address Transaction history and returns its latest transactions.

    :param driver: Web driver instance
    :param tab_name: Chrome Tab to switch to
    :param element_name: Element name wait for
    :param element_id: Element ID to scrape
    :param no_of_txns: Number of transactions to return, up to 100
    :param max_wait_time: Maximum time to wait for response
    :returns: Python Dictionary with  transactions
    """
    driver.switch_to.window(tab_name)

    try:
        WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located(
            (By.CLASS_NAME, element_name)))
    except Exception:
        return {}

    root = html.fromstring(driver.page_source)
    table = root.find_class(element_id)[0]

    # Return table as a Python Dictionary
    return scrape_table(table, no_of_txns)


def print_last_txns(
        addr_dict: dict,
        no_txns: int,
        max_wait_time: int,
) -> None:
    """
    Prints the last number of transactions for the specified addresses.

    :param addr_dict: Dictionary of addresses
    :param no_txns: No. of transactions to query and print
    :param max_wait_time: Maximum time to wait for response
    :returns: None
    """

    # Construct url and open urls
    wallet_names = []
    tab_names = []
    for address in addr_dict:
        chrome_driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_names.append(chrome_driver.window_handles[-1])
        wallet_names.append(address_dict[address]['name'])

    args = [(chrome_driver, tab, table_element_name, table_element_id, no_txns, max_wait_time)
            for tab, wallet in zip(tab_names, wallet_names)]

    for arg, address in zip(args, addr_dict):
        result = get_last_txns(*arg)

        if len(result) == 0:
            print(f"Address: {address}, {addr_dict[address]['name']}")
            print(f"Can not query website at this time, try the link - https://debank.com/profile/{address}/history\n")
            continue

        print(f"Address: {address}, {addr_dict[address]['name']}")
        for txn in result:
            print(result[txn])

        print()

    # Quit chrome driver
    chrome_driver.quit()


number_of_txns = int(input("How many of the latest transactions to print per address?: "))

filename = input("Enter name of .json file containing addresses to query: ")

with open(filename, 'r') as json_file:
    address_dict = json.load(json_file)

    print(f"Latest {number_of_txns} transactions:\n")
    # Infinite scraping. Keyboard interrupt to stop.
    print_last_txns(addr_dict=address_dict,
                    no_txns=number_of_txns,
                    max_wait_time=30)
