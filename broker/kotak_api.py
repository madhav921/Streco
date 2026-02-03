# broker/kotak_api.py
from kotakapi import KotakAPI  # example placeholder

class KotakBroker:
    def __init__(self, api_key, secret):
        self.client = KotakAPI(api_key, secret)

    def place_order(self, symbol, qty, side):
        return self.client.place_order(symbol, qty, side)
