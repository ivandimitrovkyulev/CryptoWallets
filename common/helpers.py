from lxml import html
from time import sleep
from typing import Dict
from datetime import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)
from common.message import telegram_send_message
from common.variables import CHROME_LOCATION


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


def get_last_transactions(
        driver: Chrome,
        no_of_txns: int = 20,
        wait_time: int = 15,
) -> dict:
    """
    Searches DeBank for Transaction history for an address and returns latest transactions.

    :param driver: Selenium webdriver object
    :param no_of_txns: Number of latest transactions to return
    :param wait_time: No. of secs to wait for web response
    :return: Python Dictionary with  transactions
    """
    # Wait for website to respond, if driver error raised re-try until resolved
    while True:
        try:
            WebDriverWait(driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, "History_tableLine__3dtlF")))
        except WebDriverException or TimeoutException:
            sleep(wait_time)
            driver.refresh()
        else:
            break

    root = html.fromstring(driver.page_source)
    table = root.find_class("History_table__9zhFG")[0]

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


def scrape_wallet(
        address: str,
        sleep_time: int = 30,
) -> None:
    driver = Chrome(service=Service(CHROME_LOCATION))
    # construct url and open webpage
    url = f"https://debank.com/profile/{address}/history"
    driver.get(url)

    old_txns = get_last_transactions(driver)
    while True:

        new_txns = get_last_transactions(driver)
        found_txns = dict_complement_b(old_txns, new_txns)

        # If a txn is found
        if len(found_txns) > 0:
            message = ""
            for txn in found_txns.keys():
                info = found_txns[txn]
                message = f"New Txn from {address}\n{txn}\n{info}"
                # Send Telegram message with found txns
                telegram_send_message(message)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} - {message}")

        # Update transaction dict
        old_txns = get_last_transactions(driver)

        sleep(sleep_time)
        # Try to refresh page
        try:
            driver.refresh()
        except WebDriverException as e:
            print(f"Error in {scrape_wallet.__name__}: {e}")
