# CryptoWallets v1.0.0
Screener that follows specified blockchain wallets and notifies when a new transaction occurs.


## Installation
<br/>

This project uses **Python 3.9.6** and requires a
[Chromium WebDriver](https://chromedriver.chromium.org/getting-started/) installed.

Clone the project:
```
git clone https://github.com/ivandimitrovkyulev/CryptoWallets.git

cd WalletScrape
```

Create a virtual environment in the current working directory and activate it:

```
python3 -m venv <current-directory>

source <current/directory>/bin/activate
```

Install all third-party project dependencies:
```
pip install -r requirements.txt
```

You will also need to save the following variables in a **.env** file in ../WalletScrape/common/:
```
CHROME_LOCATION=<your/web/driver/path/location> 

TOKEN=<telegram-token-for-your-bot>

CHAT_ID=<the-id-of-your-telegram-chat>
```
<br/>

## Running the script
<br/>

```
cd WalletScrape

python main.py
```
<br/>

Email: ivandkyulev@gmail.com