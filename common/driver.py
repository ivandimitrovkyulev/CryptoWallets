"""
Configure Chrome settings and initiate it.
"""
import os
from dotenv import load_dotenv
from atexit import register

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


load_dotenv()
# Get env variables
CHROME_LOCATION = os.getenv('CHROME_LOCATION')

# Chrome driver options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1400,2100')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

# Open Chromium web driver
chrome_driver = Chrome(service=Service(CHROME_LOCATION), options=options)

# Quit chrome driver after whole script has finished execution
register(chrome_driver.quit)
