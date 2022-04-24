"""
Set up program variables.
"""
import os
from dotenv import load_dotenv


load_dotenv()
# Get env variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

program_name = "wallet-scrape"

time_format = "%Y-%m-%d %H:%M:%S, %Z"

log_format = "%(asctime)s - %(levelname)s - %(message)s"

sleep_time = 120

ignore_list = (
    "play888.io",
    "gambling.io",
)
