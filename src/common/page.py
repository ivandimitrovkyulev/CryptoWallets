from lxml.html import HtmlElement

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)


from src.common.logger import log_error
from src.common.driver.driver import chrome_driver


def wait_history_table(
        element: str,
        wallet_name: str,
        wait_time: int = 30,
        max_wait_time: int = 50,
) -> None:
    """
    Waits for the presence of a HTML element located by its name.

    :param element: Element name to search for
    :param wallet_name: Name of wallet to include into logger
    :param wait_time: Seconds to wait before refreshing
    :param max_wait_time: Max seconds to wait before refreshing
    :returns: None
    """

    while True:
        try:
            WebDriverWait(chrome_driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, element)))

        except WebDriverException or TimeoutException:
            # Refresh page and log error
            chrome_driver.refresh()
            log_error.warning(f"Error while trying to load transactions for {wallet_name}")

            # Wait for longer periods
            wait_time += 5
            if wait_time >= max_wait_time:
                wait_time = max_wait_time

        # If response returned - break
        else:
            break


def scrape_table(
        table: HtmlElement,
        no_of_txns: int = 100,
) -> dict:
    """
    Scrapes an HTML table element.

    :param table: Table of <class 'lxml.html.HtmlElement'>
    :param no_of_txns: Number of transactions to return, up to 100
    :returns: Python Dictionary
    """
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
