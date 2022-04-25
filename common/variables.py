"""
Set up program variables.
"""
import os
from dotenv import load_dotenv


load_dotenv()
# Get env variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

script_name = os.path.basename(__file__)

time_format = "%Y-%m-%d %H:%M:%S, %Z"

log_format = "%(asctime)s - %(levelname)s - %(message)s"

sleep_time = 120

ignore_list = (
    "0x0000…0000",
    "play888.io",
)
