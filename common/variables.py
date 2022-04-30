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

sleep_time = 180

request_wait_time = 30

max_request_wait_time = 60

ignore_list = (
    "0x0000…0000",
    "play888.io",
)
