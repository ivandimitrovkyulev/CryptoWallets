# Set up program variables
import os
from dotenv import load_dotenv

from selenium.webdriver.chrome.options import Options


load_dotenv()
# Get env variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
CHROME_LOCATION = os.getenv('CHROME_LOCATION')

# Chrome driver options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

log_format = "%(asctime)s - %(levelname)s - %(message)s"

time_format = "%Y/%m/%d %H:%M:%S"

address_list = [
    "0x39de56518e136d472ef9645e7d6e1f7c6c8ed37b",
    "0xae653682dee958914a82c9628de794dcbbee3d04",
    "0xcba1a275e2d858ecffaf7a87f606f74b719a8a93",
    "0x9790e2f55c718a3c3d701542072d7c1d3d2e3f5f",
    "0x65bab4f268286b9005d6053a177948dddc29bad3",
]
