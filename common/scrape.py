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

from common.message import send_message
from common.driver import chrome_driver
from common.logger import log_error
from common.variables import (
    sleep_time,
    max_wait_time,
)


# Setup threading lock
lock = Lock()


def dict_complement_b(
        old_dict: dict,
        new_dict: dict,
) -> dict:
    """
    Compares dictionary A & B and returns the relative complement of A in B.
    Basically returns all members in B that are not in A as a python dictionary -
    as in Venn's diagrams.

    :param old_dict: dictionary A
    :param new_dict: dictionary B
    :returns: Python Dictionary
    """

    b_complement = {k: new_dict[k] for k in new_dict if k not in old_dict}

    return b_complement


def refresh_tab(
        tab: str,
        wait_time: int = max_wait_time,
) -> None:
    """
    Refreshes a tab given it's tab name

    :param tab: Name of driver tab
    :param wait_time: Maximum number of seconds to wait for tab refresh
    :returns: None
    """
    lock.acquire()

    # Switch to window and refresh tab
    chrome_driver.switch_to.window(tab)
    chrome_driver.execute_script("document.location.reload()")

    while True:
        try:
            WebDriverWait(chrome_driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "History_tableLine__3dtlF")))
        except WebDriverException or TimeoutException:
            # Refresh page and log error
            chrome_driver.execute_script("document.location.reload()")
            log_error.warning(f"Error while refreshing tab.")
        else:
            break

    lock.release()


def get_last_txns(
        tab_name: str,
        no_of_txns: int = 100,
        wait_time: int = max_wait_time,
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
        except WebDriverException or TimeoutException:
            # Refresh page and log error
            chrome_driver.execute_script("document.location.reload()")
            log_error.warning(f"Error while trying to load transactions.")
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

        with Pool(os.cpu_count()) as pool:
            # Get latest transactions
            old_txns = pool.starmap(get_last_txns, args_old)

            # Sleep and refresh tabs
            sleep(time_to_sleep)
            pool.map(refresh_tab, tab_names)

            # Get latest transactions
            new_txns = pool.starmap(get_last_txns, args_new)

        # Send Telegram message if txns found
        for address, old_txn, new_txn in zip(address_dict, old_txns, new_txns):
            wallet_name = address_dict[address]['name']
            chat_id = address_dict[address]['chat_id']

            # If any new txns -> send Telegram message
            found_txns = dict_complement_b(old_txn, new_txn)
            send_message(found_txns, wallet_name, chat_id)
