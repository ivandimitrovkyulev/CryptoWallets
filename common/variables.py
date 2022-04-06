# Set up program variables

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
CHROME_LOCATION = os.getenv('CHROME_LOCATION')

log_format = "%(asctime)s - %(levelname)s - %(message)s"

address_list = [
    "0x65bab4f268286b9005d6053a177948dddc29bad3",
    "0x39de56518e136d472ef9645e7d6e1f7c6c8ed37b",
    "0xae653682dee958914a82c9628de794dcbbee3d04",
    "0xcba1a275e2d858ecffaf7a87f606f74b719a8a93",
    "0x9790e2f55c718a3c3d701542072d7c1d3d2e3f5f",
]
