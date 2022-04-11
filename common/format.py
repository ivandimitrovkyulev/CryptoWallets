import re
from typing import Dict
from datetime import (
    datetime,
    timedelta,
)
from common.variables import time_format


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


def format_data(
        txn: list[list, list, list, list],
) -> list:
    """
    Takes a list of lists with transaction data and returns formatted list of information.

    :param txn: List of lists containing txn data
    :return: list with data
    """
    data = []
    if len(txn[0]) == 3:
        data.append(txn[0][0])
        txn[0].pop(0)
    else:
        try:
            time = txn[0][0]
            # Append timestamp
            if 'hr' in time and 'min' in time:
                stamps = re.findall("[0-9]+", time)
                hours = int(stamps[0])
                mins = int(stamps[1])
                time_stamp = (datetime.now() - timedelta(hours=hours, minutes=mins)).astimezone().strftime(time_format)
                data.append(time_stamp)
            elif 'min' in time and 'sec' in time:
                stamps = re.findall("[0-9]+", time)
                mins = int(stamps[0])
                secs = int(stamps[1])
                time_stamp = (datetime.now() - timedelta(minutes=mins, seconds=secs)).astimezone().strftime(time_format)
                data.append(time_stamp)
            elif 'sec' in time and 'min' not in time:
                stamps = re.findall("[0-9]+", time)
                secs = int(stamps[0])
                time_stamp = (datetime.now() - timedelta(seconds=secs)).astimezone().strftime(time_format)
                data.append(time_stamp)
            else:
                data.append(time)

        except IndexError as e:
            print(f"{e}: {txn} skipped.")

    try:
        txn_type = ""
        for item in txn[1]:
            txn_type += item + " "
        data.append(txn_type)
    except IndexError:
        data.append(txn[0])

    if len(txn[2]) == 0:
        data.append(None)
    else:
        try:
            amount = ""
            for i, item in enumerate(txn[2]):
                if i % 2 == 0:
                    amount += item + txn[2][i + 1] + " "
            data.append(amount)
        except IndexError:
            data.append(txn[2])

    return data
