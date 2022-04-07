import os
from lxml import html
from time import sleep
from typing import Dict
from datetime import datetime
from multiprocessing.dummy import Pool, Lock

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)

from common.message import telegram_send_message
from common.variables import CHROME_LOCATION


# Open Chromium web driver
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = Chrome(service=Service(CHROME_LOCATION), options=options)
# Setup threading lock
lock = Lock()


def dict_complement_b(
        old_dict: dict,
        new_dict: dict,
) -> Dict[str, list]:
    """Compares dictionary A & B and returns the relative complement of A in B.
    Basically returns all members in B that are not in A as a python dictionary -
    as in Venn's diagrams.

    :param old_dict: dictionary A
    :param new_dict: dictionary B"""

    b_complement = {k: new_dict[k] for k in new_dict if k not in old_dict}

    return b_complement


def send_message(
        address: str,
        found_txns: dict,
) -> None:
    """
    Sends a Telegram message with txns from Dictionary.

    :param address: Address to be scraping
    :param found_txns: Dictionary with transactions
    """
    # If a txn is found
    if len(found_txns) > 0:
        for txn in found_txns.keys():
            info = found_txns[txn]
            message = f"New Txn from {address}\n{txn}\n{info}"
            # Send Telegram message with found txns
            telegram_send_message(message)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} - {message}")


def refresh_tab(
        tab: str,
) -> None:
    """
    Refreshes a tab given it's tab name

    :param tab: Name of driver tab
    """
    global driver

    lock.acquire()
    driver.switch_to.window(tab)
    driver.refresh()
    lock.release()


def get_last_transactions(
        tab_name: str,
        no_of_txns: int = 50,
        wait_time: int = 15,
) -> dict:
    """
    Searches DeBank for Transaction history for an address and returns latest transactions.

    :param tab_name: Chrome Tab to switch to
    :param no_of_txns: Number of latest transactions to return
    :param wait_time: No. of secs to wait for web response
    :return: Python Dictionary with  transactions
    """
    global driver

    lock.acquire()
    driver.switch_to.window(tab_name)

    # Wait for website to respond, if driver error raised re-try until resolved
    while True:
        try:
            WebDriverWait(driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "History_tableLine__3dtlF")))
        except WebDriverException or TimeoutException:
            sleep(1)
            driver.refresh()
        else:
            break

    root = html.fromstring(driver.page_source)
    table = root.find_class("History_table__9zhFG")[0]
    lock.release()

    transactions = {}
    for index, row in enumerate(table.xpath('./div')):
        transaction = row.xpath('.//text()')
        link = row.xpath('./div/div/a/@href')[0]

        if 'Failed' in transaction:
            continue
        else:
            # Update dict with info
            transactions[link] = transaction

        if index >= (no_of_txns - 1):
            break

    return transactions


def scrape_wallets(
        address_list: list,
        sleep_time: int = 60,
) -> None:

    # construct url and open webpage
    tab_names = []
    for address in address_list:
        driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_name = driver.window_handles[-1]
        tab_names.append(tab_name)

    while True:
        with Pool(os.cpu_count()) as pool:
            old_txns = pool.map(get_last_transactions, tab_names)

            # Sleep and refresh tabs
            sleep(sleep_time)
            pool.map(refresh_tab, tab_names)

            new_txns = pool.map(get_last_transactions, tab_names)

            # Send Telegram message if txns found
            for address, old_txn, new_txn in zip(address_list, old_txns, new_txns):
                # If any new txns -> send Telegram message
                found_txns = dict_complement_b(old_txn, new_txn)
                send_message(address, found_txns)
