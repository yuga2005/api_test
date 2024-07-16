# <!-- Problem Statement You are tasked with developing a Python application that monitors cryptocurrency prices from an API and alerts the user when certain price conditions are met. The application will primarily focus on Bitcoin, using data from the CoinDesk API. You will utilize the endpoint `https://api.coindesk.com/v1/bpi/currentprice.json` to fetch the current price of Bitcoin in USD, and determine if it has crossed specified high or low price thresholds.
# 1. **API Interaction**: - Fetch the current Bitcoin price in USD from the CoinDesk API (`https://api.coindesk.com/v1/bpi/currentprice.json`). This API provides a JSON response containing various details, including the updated price of Bitcoin in multiple currencies. - Parse the JSON to extract the current Bitcoin price in USD.
 
# 2. **Configuration**: - Allow the user to set upper and lower price thresholds through the command line or a configuration file. For example: ```python price_thresholds
# Note: Due to duration of interview, choose limits close to what the value is so we can get the value to cross.
 
# 3. **Monitoring and Alerts**: - Continuously monitor the price at regular intervals (e.g., every 30 seconds). - Check if the current price crosses any of the set thresholds. - If a threshold is crossed, print an alert message and possibly log this event, e.g.: ``` Alert: Bitcoin price has risen above threshold “x” ```
 
# 4. **Logging and Storage**: - Log every API call, including the timestamp, the API endpoint, and the current Bitcoin price retrieved. - Optionally, keep a log or a temporary record of all price checks for the duration the application runs.
 
# 5. **Error Handling**: - Implement robust error handling to manage scenarios such as API downtimes, rate limits, or malformed responses. - Ensure the application can recover from an error without exiting or crashing.

# has context menu -->

import requests
import time
import logging
from datetime import datetime


logging.basicConfig(filename='bitcoin_price_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_bitcoin_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    try:
        response = requests.get(url)
        if response.status_code == 429:
            logging.warning('Rate limit exceeded. Waiting for 60 seconds.')
            time.sleep(60)
            return None
        response.raise_for_status()  
        data = response.json()
        if 'bpi' in data and 'USD' in data['bpi'] and 'rate_float' in data['bpi']['USD']:
            price = data['bpi']['USD']['rate_float']
            return price
        else:
            logging.error('Unexpected response structure: Missing "rate_float" in "bpi"')
            return None
    except requests.RequestException as e:
        logging.error(f'Error fetching Bitcoin price: {e}')
        return None


def check_price(price, lower_threshold, upper_threshold):
    if price < lower_threshold:
        logging.info(f'Alert: Bitcoin price has fallen below the threshold ${lower_threshold:.2f}')
        print(f'Alert: Bitcoin price has fallen below the threshold ${lower_threshold:.2f}')
    elif price > upper_threshold:
        logging.info(f'Alert: Bitcoin price has risen above the threshold ${upper_threshold:.2f}')
        print(f'Alert: Bitcoin price has risen above the threshold ${upper_threshold:.2f}')
    else:
        logging.info(f'Bitcoin price is within thresholds: ${price:.2f}')


def monitor_price(lower_threshold, upper_threshold, interval=30):
    while True:
        price = fetch_bitcoin_price()
        if price is not None:
            logging.info(f'Current Bitcoin price: ${price:.2f}')
            check_price(price, lower_threshold, upper_threshold)
        else:
            logging.warning('Failed to fetch Bitcoin price. Retrying in the next interval.')
        time.sleep(interval)

if __name__ == '__main__':
    lower_threshold = 29000.0  
    upper_threshold = 31000.0  

    logging.info('Starting Bitcoin price monitor')
    monitor_price(lower_threshold, upper_threshold)

