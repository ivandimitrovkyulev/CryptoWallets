import os
from lxml import html
from time import sleep

from multiprocessing.dummy import (
    Pool,
    Lock,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)

from common.format import dict_complement_b
from common.message import send_message
from common.driver import chrome_driver
from common.logger import logg_error
from common.variables import sleep_time


# Setup threading lock
lock = Lock()


def print_last_transactions(
        address_dict: dict,
        no_of_txns: int = 3,
) -> None:

    # construct url and open webpage
    tab_names = []
    for address in address_dict:
        chrome_driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_names.append(chrome_driver.window_handles[-1])

    args = [(tab, no_of_txns) for tab in tab_names]

    with Pool(os.cpu_count()) as pool:
        batch = pool.starmap(get_last_transactions, args)

        for transactions, address in zip(batch, address_dict):

            print(f"Address: {address}, {address_dict[address]['name']}")
            for info in transactions:
                txn_details = transactions[info]
                print(txn_details)

            print()

    # Quit chrome driver
    chrome_driver.quit()


def refresh_tab(
        tab: str,
) -> None:
    """
    Refreshes a tab given it's tab name

    :param tab: Name of driver tab
    :returns: None
    """

    lock.acquire()

    # Switch to window and refresh tab
    chrome_driver.switch_to.window(tab)
    chrome_driver.refresh()

    lock.release()


def get_last_transactions(
        tab_name: str,
        no_of_txns: int = 100,
        wait_time: int = 20,
) -> dict:
    """
    Searches DeBank for Transaction history for an address and returns latest transactions.

    :param tab_name: Chrome Tab to switch to
    :param no_of_txns: Number of latest transactions to return
    :param wait_time: No. of secs to wait for web response
    :return: Python Dictionary with  transactions
    """

    lock.acquire()
    chrome_driver.switch_to.window(tab_name)

    # Wait for website to respond, if driver error raised re-try until resolved
    while True:
        try:
            WebDriverWait(chrome_driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "History_tableLine__3dtlF")))
        except WebDriverException or TimeoutException as e:
            sleep(1)
            chrome_driver.refresh()
            logg_error.warning(f"{e} - Error while trying to load transactions. Refreshing Tab.")
        else:
            break

    root = html.fromstring(chrome_driver.page_source)
    table = root.find_class("History_table__9zhFG")[0]
    lock.release()

    transactions = {}
    for index, row in enumerate(table.xpath('./div')):
        # If limit reached, break
        if index >= int(no_of_txns):
            break

        # Get link to transaction
        link = row.xpath('./div/div/a/@href')[0]

        txn_list = []
        for col in row.xpath('./div'):
            # Get text for Txn, Type, Amount, Gas fee
            info = col.xpath('.//text()')
            txn_list.append(info)

        if len(txn_list) >= 4:
            transactions[link] = txn_list

    return transactions


def scrape_multiple_wallets(
        address_dict: dict,
        time_to_sleep: int = sleep_time,
) -> None:
    """
    Constantly scrapes multiple addresses and sends a Telegram message if new transaction is detected.

    :param address_dict: Dictionary of addresses where keys are '0x63dhf6...9vs5' values
    :param time_to_sleep: Time to sleep between queries
    :return: None
    """

    # construct url and open webpage
    tab_names = []
    for address in address_dict:
        chrome_driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_names.append(chrome_driver.window_handles[-1])

    args_old = [(tab, 100) for tab in tab_names]
    args_new = [(tab, 50) for tab in tab_names]

    while True:
        # Multi-scrape all addresses for txns
        with Pool(os.cpu_count()) as pool:
            old_txns = pool.starmap(get_last_transactions, args_old)

            # Sleep and refresh tabs
            sleep(time_to_sleep)
            pool.map(refresh_tab, tab_names)

            new_txns = pool.starmap(get_last_transactions, args_new)

        # Send Telegram message if txns found
        for address, old_txn, new_txn in zip(address_dict, old_txns, new_txns):
            wallet_name = address_dict[address]['name']
            # If any new txns -> send Telegram message
            found_txns = dict_complement_b(old_txn, new_txn)
            send_message(wallet_name, found_txns)
