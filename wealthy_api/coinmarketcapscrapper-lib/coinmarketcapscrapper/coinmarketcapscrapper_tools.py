import re
import requests
import collections
from bs4 import BeautifulSoup
from decimal import InvalidOperation

from datetime import datetime


Resource = collections.namedtuple('Resource', ['ticker_from', 'ticker_to', 'price', 'timestamp'])

class CoinMarketCapScrapper(object):

    URL = 'https://coinmarketcap.com/currencies/{crypto}/'
    crypto_mapping = {
        'FLM': 'flamingo'
    }

    def __init__(self):
        pass

    def fetch_crypto_price(self, crypto):
        name = self.crypto_mapping.get(crypto)
        try:
            page = requests.get(self.URL.format(crypto=name))
        except requests.exceptions.ConnectionError as e:
            print(e)
            return None
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            spans = soup.find_all('span', attrs={'class': 'cmc-details-panel-price__price'})

            if not spans:
                print("Spans not found.")
                return None

            if len(spans) > 1:
                print("More than one element, Need to settle which is appropriate.")
                return None

            text = spans[0].string
            text = re.sub(',', '', text)
            price = text[1:]
        except (AttributeError, KeyError, IndexError, InvalidOperation) as e:
            print(e)
            return None
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y, %H:%M:%S")
        return Resource(ticker_from=crypto, ticker_to='USD', price=price, timestamp=timestamp)


if __name__ == '__main__':
    fetcher = CoinMarketCapScrapper()
    crypto_price = fetcher.fetch_crypto_price("FLM")
    print(crypto_price)
