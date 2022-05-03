import os

from subprocess import Popen
from multiprocessing.dummy import Pool

from single_scrape import file_name


def scrape_wallets_subprocess(
        address_dict: dict,
) -> None:
    """
    Constantly scrapes multiple addresses and sends a Telegram message if new transaction is detected.

    :param address_dict: Dictionary of addresses where keys are '0x63dhf6...9vs5' values
    :return: None
    """

    # construct arguments and open webpages
    args = [["python3", f"{file_name}", f"{address}", f"{address_dict[address]}"]
            for address in address_dict]

    with Pool(os.cpu_count()) as pool:
        # Open multiple subprocesses to scrape wallets
        processes = pool.map(Popen, args)

        for process in processes:
            process.communicate()
