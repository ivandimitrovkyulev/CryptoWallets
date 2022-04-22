"""
Set up program variables.
"""
import os
from dotenv import load_dotenv


load_dotenv()
# Get env variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

log_format = "%(asctime)s - %(levelname)s - %(message)s"

time_format = "%Y-%m-%d %H:%M:%S, %Z"

sleep_time = 60
