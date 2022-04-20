import json


# Dictionary of addresses
wallets = {
    "0xeaa4f3773f57af1d4c7130e07cde48050245511b": {"id": "1", "name": "silly"},
    "0xa0f75491720835b36edc92d06ddc468d201e9b73": {"id": "2", "name": "analytico"},
    "0x0f763341b448bb0f02370f4037fe4a2c84c9283f": {"id": "3", "name": "dcfgod1"},
    "0x39DE56518e136d472Ef9645e7D6E1F7c6C8Ed37b": {"id": "4", "name": "cyi"},
    "0xa42830ee059c77caf8c8200b44aa9813cb0720c5": {"id": "5", "name": "a1"},
    "0xce0e4b5d659a7ffb0d6eb5171515f4833cf21721": {"id": "6", "name": "a2"},
    "0xca86d57519dbfe34a25eef0923b259ab07986b71": {"id": "7", "name": "messiah"},
}

filename = 'wallets.json'
# Save to text file
with open(filename, 'w') as file:
    json.dump(wallets, file, indent=4)
