from typing import Optional
from datetime import datetime

from requests import (
    post,
    Response
)

from common.format import format_data
from common.variables import (
    TOKEN,
    CHAT_ID,
    time_format,
)


def telegram_send_message(
        message_text: str,
        disable_web_page_preview: bool = True,
        telegram_token: Optional[str] = "",
        telegram_chat_id: Optional[str] = "",
) -> Response:
    """
    Sends a Telegram message to a specified chat.
    Must have a .env file with the following variables:
    TOKEN: your Telegram access token.
    CHAT_ID: the specific id of the chat you want the message sent to
    Follow telegram's instruction on how to set up a bot using the bot father
    and configure it to be able to send messages to a chat.

    :param message_text: Text to be sent to the chat
    :param disable_web_page_preview: Set web preview on/off
    :param telegram_token: Telegram TOKEN API, default take from .env
    :param telegram_chat_id: Telegram chat ID, default take from .env
    :return: requests.Response
    """

    # if URL not provided - try TOKEN variable from the .env file
    if telegram_token == "":
        telegram_token = TOKEN

    # if chat_id not provided - try CHAT_ID variable from the .env file
    if telegram_chat_id == "":
        telegram_chat_id = CHAT_ID

    # construct url using token for a sendMessage POST request
    url = "https://api.telegram.org/bot{}/sendMessage".format(telegram_token)

    # Construct data for the request
    data = {"chat_id": telegram_chat_id, "text": message_text,
            "disable_web_page_preview": disable_web_page_preview}

    # send the POST request
    post_request = post(url, data)

    return post_request


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
            # Format dict value
            info = format_data(found_txns[txn])

            # Construct message string
            formatted_info = ""
            for item in info:
                formatted_info += f"         {item}\n"
            message = f"New txn from {address}:\n{txn}\nDetails: \n{formatted_info}"

            # Send Telegram message with found txns
            telegram_send_message(message)

            # Print result to terminal
            timestamp = datetime.now().astimezone().strftime(time_format)
            print(f"{timestamp} - {message}")
