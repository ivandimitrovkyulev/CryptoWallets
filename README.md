# CryptoWallets v1.0.0
Screener that follows specified blockchain wallets and notifies when a new transaction occurs.


## Installation
<br/>

This project uses **Python 3.9.6** and requires a
[Chromium WebDriver](https://chromedriver.chromium.org/getting-started/) installed.

Clone the project:
```
git clone https://github.com/ivandimitrovkyulev/CryptoWallets.git

cd CryptoWallets
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

You will also need to save the following variables in a **.env** file in ../CryptoWallets:
```
CHROME_LOCATION=<your/web/driver/path/location> 

TOKEN=<telegram-token-for-your-bot>

CHAT_ID=<the-id-of-your-telegram-chat>
```
<br/>

## Running the script
<br/>

```
cd CryptoWallets
```
Create a **wallets.json** file with addresses of the following structure:

```
{
    "0xa42830ee059c17caf3c8200b44aa9813cb0720c5": {
        "name": "CoinBase",
        ...,
        ...,
    },
    "0xce0e4b5d659a7ffb0d6eb5271515f4833cf21129": {
        "name": "Binance",
        ...,
        ...,
    },
    "0xca86d57519dbff34a28eef0923b259ab07986b87": {
        "name": "Crypto.com",
        ...,
        ...,
    }
}
```
Save the contants of **wallets.json** file in a variable:
```
var="$(cat wallets.json)"
```
Now you can run the script by passing the addresses to screen:
```
python main.py "$var"
```

<br/>

## Docker deployment
<br/>

Build a docker image named **wallet-scrape**:
```
cd CryptoWallets
docker build . -t wallet-scrape
```
Run docker container:
```
var="$(cat wallets.json)"
docker run --shm-size=2g -it <image-id> python3 main.py "$var"  
```

where **--shm-size=2g** docker argument is provided to prevent Chromium from the **"from tab crashed"** error.

<br/>
<br/>

Email: ivandkyulev@gmail.com