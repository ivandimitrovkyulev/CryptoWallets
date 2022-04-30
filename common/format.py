import re
from typing import Optional
from datetime import (
    datetime,
    timedelta,
)
from common.logger import (
    log_spam,
    log_error,
)
from common.variables import (
    time_format,
    ignore_list,
)


def format_data(
        txn: list[list, list, list, list],
        time_diff_hours: int = 3,
        time_diff_mins: int = 0,
) -> Optional[list]:
    """
    Takes a list of lists with transaction data and returns formatted list of information.

    :param txn: List of lists containing txn data.
    :param time_diff_hours: Skips transactions that occurred more than specified hours ago.
    :param time_diff_mins: Skips transactions that occurred more than specified mins ago.
    :return: List with formatted data or None if Txn does not meet criteria
    """
    data = []

    # If txn does not have the right structure
    if isinstance(txn, list) is False:
        log_error.critical(f"{txn} is not a list.")
        return
    elif len(txn) != 4:
        log_error.critical(f"{txn} length does not equal 4.")
        return
    else:
        for item in txn:
            if isinstance(item, list) is False:
                log_error.critical(f"{txn} is not a list of lists.")
                return

    # If txn failed return none
    if 'Failed' in txn[0]:
        return

    # If txn from unwanted address return none
    for item in txn[1]:
        if item in ignore_list:
            log_spam.info(f"{txn}")
            return

    # Log all Receive txns for analyses
    if "Receive" in txn[1]:
        log_spam.info(f"{txn}")

    # Format txn time
    try:
        time = txn[0][0]
        now = datetime.now()

        # Append timestamp
        if 'hr' in time and 'min' in time:
            stamps = re.findall("[0-9]+", time)
            hours = int(stamps[0])
            mins = int(stamps[1])

            time_stamp = now - timedelta(hours=hours, minutes=mins)

            # Append formatted time to list
            data.append(time_stamp.astimezone().strftime(time_format))

        elif 'min' in time and 'sec' in time:
            stamps = re.findall("[0-9]+", time)
            mins = int(stamps[0])
            secs = int(stamps[1])

            time_stamp = now - timedelta(minutes=mins, seconds=secs)

            # Append formatted time to list
            data.append(time_stamp.astimezone().strftime(time_format))

        elif 'sec' in time and 'min' not in time:
            stamps = re.findall("[0-9]+", time)
            secs = int(stamps[0])

            time_stamp = now - timedelta(seconds=secs)

            # Append formatted time to list
            data.append(time_stamp.astimezone().strftime(time_format))

        else:
            time_stamp = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
            data.append(time)

        # If transaction occurred more that time_difference - skip
        if now - time_stamp > timedelta(hours=time_diff_hours, minutes=time_diff_mins):
            log_spam.info(f"{txn} time is old.")
            return
    except TypeError or IndexError as e:
        # log skipped txn
        log_error.critical(f"{e}: {txn} timestamp is missing.")
        return

    # Format txn type
    try:
        txn_type = "Type: "
        for item in txn[1]:
            txn_type += f"{item} "
        data.append(txn_type)
    except IndexError:
        data.append(txn[1])

    # Format txn amount
    if len(txn[2]) == 0:
        data.append("Swap: None")
    else:
        try:
            amount = "Swap: "
            for i, item in enumerate(txn[2]):
                if i % 2 == 0:
                    amount += item + txn[2][i + 1] + " "
            data.append(amount)
        except IndexError:
            data.append(txn[2])

    return data
