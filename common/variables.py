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
options.add_argument('--no-sandbox')
options.add_argument('window-size=1400,2100')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

log_format = "%(asctime)s - %(levelname)s - %(message)s"

time_format = "%Y-%m-%d %H:%M:%S, %Z"
