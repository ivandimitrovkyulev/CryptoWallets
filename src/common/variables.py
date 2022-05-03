"""
Set up program variables.
"""
import os
from dotenv import load_dotenv


load_dotenv()
# Get env variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


time_format = "%Y-%m-%d %H:%M:%S, %Z"

log_format = "%(asctime)s - %(levelname)s - %(message)s"

# Amount of time to sleep after each scrape
sleep_time = 180

# Time to wait for page to respond
request_wait_time = 30

# Max time to wait for page to respond
max_request_wait_time = 50

# List of strings to ignore if contained in the transaction info
ignore_list = (
    "0x0000…0000",
    "play888.io",
)
