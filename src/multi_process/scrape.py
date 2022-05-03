import os
from time import sleep
from lxml import html
from multiprocessing.dummy import Pool, Lock

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)
from src.common.logger import log_error
from src.common.format import dict_complement_b
from src.common.message import send_message
from src.common.driver import chrome_driver
from src.common.variables import (
    request_wait_time,
    max_request_wait_time,
    sleep_time,
)


# Setup threading lock
lock = Lock()


def refresh_tab(
        tab_name: str,
        wallet_name: str,
        wait_time: int = request_wait_time,
) -> None:
    """
    Refreshes a tab given it's tab name

    :param tab_name: Name of driver tab
    :param wallet_name: Name of wallet to scrape
    :param wait_time: Maximum number of seconds to wait for tab refresh
    :returns: None
    """
    lock.acquire()

    # Switch to window and refresh tab
    chrome_driver.switch_to.window(tab_name)
    chrome_driver.execute_script("document.location.reload()")

    while True:
        try:
            WebDriverWait(chrome_driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "History_tableLine__3dtlF")))
        except WebDriverException or TimeoutException:
            # Refresh page and log error
            chrome_driver.execute_script("document.location.reload()")
            log_error.warning(f"Error while refreshing tab for {wallet_name}")
        else:
            break

    lock.release()


def get_last_txns(
        tab_name: str,
        wallet_name: str,
        no_of_txns: int = 100,
        wait_time: int = request_wait_time,
) -> dict:
    """
    Searches DeBank for Transaction history for an address and returns latest transactions.

    :param tab_name: Chrome Tab to switch to
    :param wallet_name: Name of wallet to scrape
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
            log_error.warning(f"Error while trying to load transactions for {wallet_name}")
            wait_time += 5
        else:
            break

        # Wait for longer periods
        if wait_time >= max_request_wait_time:
            wait_time = request_wait_time

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


def scrape_wallets_multiprocess(
        address_dict: dict,
) -> None:
    """
    Constantly scrapes multiple addresses and sends a Telegram message if new transaction is detected.

    :param address_dict: Dictionary of addresses where keys are '0x63dhf6...9vs5' values
    :return: None
    """

    # construct url and open webpage
    tab_names = []
    wallet_names = []
    for address in address_dict:
        chrome_driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_names.append(chrome_driver.window_handles[-1])
        wallet_names.append(address_dict[address]['name'])

    args_old = [(tab, wallet, 100) for tab, wallet in zip(tab_names, wallet_names)]
    args_new = [(tab, wallet, 50) for tab, wallet in zip(tab_names, wallet_names)]
    args_refresh = [(tab, wallet) for tab, wallet in zip(tab_names, wallet_names)]

    while True:

        with Pool(os.cpu_count()) as pool:
            # Get latest transactions
            old_txns = pool.starmap(get_last_txns, args_old)

            # Sleep and refresh tabs
            sleep(sleep_time)
            pool.starmap(refresh_tab, args_refresh)

            # Get latest transactions
            new_txns = pool.starmap(get_last_txns, args_new)

        # Send Telegram message if txns found
        for address, old_txn, new_txn in zip(address_dict, old_txns, new_txns):
            wallet_name = address_dict[address]['name']
            chat_id = address_dict[address]['chat_id']

            # If any new txns -> send Telegram message
            found_txns = dict_complement_b(old_txn, new_txn)
            send_message(found_txns, wallet_name, chat_id)
