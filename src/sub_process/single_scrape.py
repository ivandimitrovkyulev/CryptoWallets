import os
import sys
import ast

from lxml import html
from time import sleep
from dotenv import load_dotenv
from atexit import register

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)

from src.common.exceptions import exit_handler
from src.common.logger import log_error
from src.common.message import send_message
from src.common.format import dict_complement_b

from src.common.variables import (
    request_wait_time,
    sleep_time,
)


if len(sys.argv) != 3:
    sys.exit("Please provide 2 arguments: [Address] & [address info dictionary].")

address = sys.argv[1]

address_dict = ast.literal_eval(sys.argv[2])
name = address_dict['name']
chat = address_dict['chat_id']


# Register function to be executed when script terminates
program_name = f"{os.path.basename(__file__)} - {name} wallet"
register(exit_handler, program_name)

load_dotenv()
# Get env variables
CHROME_LOCATION = os.getenv('CHROME_LOCATION')

# Chrome driver options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1400,2100')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

# Open chrome web driver
chrome_driver = Chrome(service=Service(CHROME_LOCATION), options=options)
chrome_driver.get(f"https://debank.com/profile/{address}/history")


def refresh_tab(
        wallet_name: str,
        wait_time: int = request_wait_time,
) -> None:
    """
    Refreshes a tab given it's tab name

    :param wallet_name: Name of wallet to scrape
    :param wait_time: Maximum number of seconds to wait for tab refresh
    :returns: None
    """

    # Refresh tab
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


def get_last_txns(
        wallet_name: str,
        no_of_txns: int = 100,
        wait_time: int = request_wait_time,
) -> dict:
    """
    Searches DeBank for Transaction history for an address and returns latest transactions.

    :param wallet_name: Name of wallet to scrape
    :param no_of_txns: Number of latest transactions to return
    :param wait_time: No. of secs to wait for web response
    :return: Python Dictionary with  transactions
    """

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

    root = html.fromstring(chrome_driver.page_source)
    table = root.find_class("History_table__9zhFG")[0]

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


def scrape_single_wallet(
        wallet_name: str,
        chat_id: str,
        time_to_sleep: int = sleep_time,
):
    """
    Scrapes a single wallet address.

    :param wallet_name: Name of wallet
    :param chat_id: Telegram chat ID to send messages to
    :param time_to_sleep: Time to sleep between queries
    :returns: None
    """

    while True:
        # Get latest transactions
        old_txns = get_last_txns(wallet_name, 100)

        # Sleep and refresh tab
        sleep(time_to_sleep)
        refresh_tab(wallet_name)

        # Get latest transactions
        new_txns = get_last_txns(wallet_name, 50)

        # If any new txns -> send Telegram message
        found_txns = dict_complement_b(old_txns, new_txns)
        send_message(found_txns, wallet_name, chat_id)


# Start screening single wallet address
scrape_single_wallet(name, chat)
