import os
from lxml import html
from time import sleep

from multiprocessing.dummy import (
    Pool,
    Lock,
)

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)

from common.format import dict_complement_b
from common.message import send_message
from common.variables import (
    CHROME_LOCATION,
    options,
)


# Open Chromium web driver
driver = Chrome(service=Service(CHROME_LOCATION), options=options)
# Setup threading lock
lock = Lock()


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
        no_of_txns: int = 100,
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
        # If limit reached, break
        if index >= (no_of_txns - 1):
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
        address_list: list,
        sleep_time: int = 60,
) -> None:

    # construct url and open webpage
    tab_names = []
    for address in address_list:
        driver.execute_script(f"window.open('https://debank.com/profile/{address}/history')")
        tab_names.append(driver.window_handles[-1])

    args_old = [(tab, 100) for tab in tab_names]
    args_new = [(tab, 50) for tab in tab_names]

    while True:
        with Pool(os.cpu_count()) as pool:
            old_txns = pool.starmap(get_last_transactions, args_old)

            # Sleep and refresh tabs
            sleep(sleep_time)
            pool.map(refresh_tab, tab_names)

            new_txns = pool.starmap(get_last_transactions, args_new)

            # Send Telegram message if txns found
            for address, old_txn, new_txn in zip(address_list, old_txns, new_txns):
                # If any new txns -> send Telegram message
                found_txns = dict_complement_b(old_txn, new_txn)
                send_message(address, found_txns)
