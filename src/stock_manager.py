# src/stock_manager.py
import requests
import pandas as pd
from typing import Set
import logging
import time

class StockManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.symbols: Set[str] = set()
        self.last_update = 0
        self.update_interval = 24 * 60 * 60  # 24 hours in seconds

    def get_stock_symbols(self) -> Set[str]:
        """Retrieve and perpetually cache stock symbols from Alpha Vantage"""
        current_time = time.time()
        if not self.symbols or (current_time - self.last_update) > self.update_interval:
            try:
                url = f"{self.base_url}?function=LISTING_STATUS&apikey={self.api_key}"
                df = pd.read_csv(url)
                self.symbols = set(df[df['assetType'] == 'Stock']['symbol'].values)
                self.last_update = current_time
                logging.info(f"Updated stock symbols. Total count: {len(self.symbols)}")
            except Exception as e:
                logging.error(f"Failed to retrieve stock symbols: {e}")
                if not self.symbols:
                    raise
        return self.symbols
