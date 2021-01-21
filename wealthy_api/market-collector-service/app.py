import time
from decimal import Decimal
from mongomarket import mongomarket_tools
from alphavantage import alphavantage_tools
from coinmarketcapscrapper import coinmarketcapscrapper_tools


class AvMarketCollector:
    def __init__(self):
        self.api = alphavantage_tools.AvAPI()
        self.coin_market_cap = coinmarketcapscrapper_tools.CoinMarketCapScrapper()

    def get_market_data_from_api(self):
        print("Start query api endpoints...")
        self.gold = self.api.get_resource(from_currency='XAU', to_currency='USD')
        self.silver = self.api.get_resource(from_currency='XAG', to_currency='USD')

        self.usdpln = self.api.get_resource(from_currency='USD', to_currency='PLN')
        self.usdeur = self.api.get_resource(from_currency='USD', to_currency='EUR')
        self.usdchf = self.api.get_resource(from_currency='USD', to_currency='CHF')

        self.btc = self.api.get_resource(from_currency='BTC', to_currency='USD')
        self.bch = self.api.get_resource(from_currency='BCH', to_currency='USD')
        self.eth = self.api.get_resource(from_currency='ETH', to_currency='USD')
        self.xrp = self.api.get_resource(from_currency='XRP', to_currency='USD')
        self.ltc = self.api.get_resource(from_currency='LTC', to_currency='USD')
        self.dot = self.api.get_resource(from_currency='DOT', to_currency='USD')
        self.neo = self.api.get_resource(from_currency='NEO', to_currency='USD')
        self.theta = self.api.get_resource(from_currency='THETA', to_currency='USD')
        self.flm = self.coin_market_cap.fetch_crypto_price("FLM")

    def collect_crypto_records(self):
        self._collect_crypto_record(self.btc)
        self._collect_crypto_record(self.bch)
        self._collect_crypto_record(self.eth)
        self._collect_crypto_record(self.xrp)
        self._collect_crypto_record(self.ltc)
        self._collect_crypto_record(self.dot)
        self._collect_crypto_record(self.neo)
        self._collect_crypto_record(self.flm)
        self._collect_crypto_record(self.theta)

    def _collect_crypto_record(self, crypto_resource_obj=None):
        records = []
        if crypto_resource_obj:
            val = Decimal(crypto_resource_obj.price)
            value = str(val.__round__(2))
            records.append({'name': crypto_resource_obj.ticker_from.lower(), 'currency': 'USD', 'value': value})
            if self.usdchf:
                val = Decimal(crypto_resource_obj.price) * Decimal(self.usdchf.price)
                value = str(val.__round__(2))
                records.append({'name': crypto_resource_obj.ticker_from.lower(), 'currency': 'CHF', 'value': value})
            if self.usdeur:
                val = Decimal(crypto_resource_obj.price) * Decimal(self.usdeur.price)
                value = str(val.__round__(2))
                records.append({'name': crypto_resource_obj.ticker_from.lower(), 'currency': 'EUR', 'value': value})
            if self.usdpln:
                val = Decimal(crypto_resource_obj.price) * Decimal(self.usdpln.price)
                value = str(val.__round__(2))
                records.append({'name': crypto_resource_obj.ticker_from.lower(), 'currency': 'PLN', 'value': value})
        for r in records:
            self._set_mongo_crypto_data(r)

    def collect_metal_records(self):
        if self.gold:
            self._collect_gold_records(self.gold.price, 'USD', 1.0)
            if self.usdeur:
                self._collect_gold_records(self.gold.price, self.usdeur.ticker_to, self.usdeur.price)
            if self.usdchf:
                self._collect_gold_records(self.gold.price, self.usdchf.ticker_to, self.usdchf.price)
            if self.usdpln:
                self._collect_gold_records(self.gold.price, self.usdpln.ticker_to, self.usdpln.price)

        if self.silver:
            self._collect_silver_records(self.silver.price, 'USD', 1.0)
            if self.usdeur:
                self._collect_silver_records(self.silver.price, self.usdeur.ticker_to, self.usdeur.price)
            if self.usdchf:
                self._collect_silver_records(self.silver.price, self.usdchf.ticker_to, self.usdchf.price)
            if self.usdpln:
                self._collect_silver_records(self.silver.price, self.usdpln.ticker_to, self.usdpln.price)

    def _collect_gold_records(self, api_gold_999_oz_usd_value, currency, exchange_rate):
        """
        collect dict in format {name: val, oz: val, g: val, kg: val}, like e.g:
        {'name': 'gold999', 'oz': '1907.22', 'g': '61.33', 'kg': '61317.28'}
        then assign it to records.
        """
        records = []
        units = ['oz', 'g', 'kg']
        gold_trials = ['999', '585', '333']

        for trial in gold_trials:
            d = {}
            oz_value = Decimal(api_gold_999_oz_usd_value) * Decimal(exchange_rate)
            # in case of 585 and 333 take into account higher spread.
            if trial == '585' or trial == '333':
                oz_value = oz_value * Decimal(0.95)
            val = self._convert_price_from_999_to_other(trial, oz_value)
            ls = [self._convert_price_from_oz_to_other_unit(val, u) for u in units]
            z = list(zip(units, ls))
            d["name"] = "gold" + trial
            d["currency"] = currency
            d.update(dict(z))

            for u in units:
                records.append({'name': d.get('name'), 'unit': u, 'currency': d.get('currency'), 'value': d.get(u)})

        # collect market data to mongo database
        for r in records:
            self._set_mongo_metal_data(r)

    def _collect_silver_records(self, api_silver_999_oz_usd_value, currency, exchange_rate):
        records = []
        units = ['oz', 'g', 'kg']
        silver_trials = ['999', '800']

        for trial in silver_trials:
            d = {}
            oz_value = Decimal(api_silver_999_oz_usd_value) * Decimal(exchange_rate)
            # in case of 800 take into account higher spread.
            if trial == '800':
                oz_value = oz_value * Decimal(0.75)
            val = self._convert_price_from_999_to_other(trial, oz_value)
            ls = [self._convert_price_from_oz_to_other_unit(val, u) for u in units]
            z = list(zip(units, ls))
            d["name"] = "silver" + trial
            d["currency"] = currency
            d.update(dict(z))

            for u in units:
                records.append({'name': d.get('name'), 'unit': u, 'currency': d.get('currency'), 'value': d.get(u)})

        # collect market data to mongo database
        for r in records:
            self._set_mongo_metal_data(r)

    @staticmethod
    def _set_mongo_metal_data(record):
        if not record.get('name') and not record.get('unit') and not record.get('currency') and not record.get('value'):
            return
        mongomarket_tools.set_metal_price(
            name=record.get('name'),
            unit=record.get('unit'),
            currency=record.get('currency'),
            value=record.get('value'))

    @staticmethod
    def _set_mongo_crypto_data(record):
        if not record.get('name') and not record.get('currency') and not record.get('value'):
            return
        mongomarket_tools.set_crypto_price(
            name=record.get('name'),
            currency=record.get('currency'),
            value=record.get('value'))

    @staticmethod
    def _convert_price_from_oz_to_other_unit(oz_price, unit_to):
        value = None
        try:
            if unit_to == 'oz':
                value = Decimal(oz_price).__round__(2)
            if unit_to == 'kg':
                val = Decimal(oz_price) * Decimal(32.15)
                value = val.__round__(2)
            if unit_to == 'g':
                val = Decimal(oz_price) / Decimal(31.1)
                value = val.__round__(2)
        except TypeError:
            return value
        return str(value)

    @staticmethod
    def _convert_price_from_999_to_other(trial: str, price: str) -> str:
        if trial == "999":
            return price
        convert_price = Decimal(price) * (Decimal(trial) / 1000)
        return str(convert_price.__round__(2))


def alpha_vantage_market():
    collector = AvMarketCollector()

    while True:
        collector.get_market_data_from_api()
        collector.collect_metal_records()
        collector.collect_crypto_records()

        documents = mongomarket_tools.get_content('metals')
        print("Metals collection:")
        for doc in documents:
            print(doc)
        print(" ")

        documents = mongomarket_tools.get_content('cryptos')
        print("Cryptos collection:")
        for doc in documents:
            print(doc)
        print(" ")
        print(" ")
        print("go to sleep ")
        time.sleep(10)


if __name__ == '__main__':
    alpha_vantage_market()
