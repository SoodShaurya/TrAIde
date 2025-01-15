# src/stock_manager.py
import pandas as pd
import logging
import time
import os

from typing import Set

class StockManager:
    def __init__(self, config):
        self.base_url = "https://www.alphavantage.co/query"
        self.symbols: Set[str] = set()
        self.last_update = 0
        self.update_interval = 24 * 60 * 60  # 24 hours in seconds
        self.config = config

    def get_stock_symbols(self) -> Set[str]:
        """Retrieve and perpetually cache stock symbols from Alpha Vantage"""
        current_time = time.time()
        if not self.symbols or (current_time - self.last_update) > self.update_interval:
            try:
                url = f"{self.base_url}?function=LISTING_STATUS&apikey={self.config['ALPHA_VANTAGE']['API_KEY']}"
                df = pd.read_csv(url)
                df.to_csv("./data/listing_status.csv")
                # df = pd.read_csv("./data/listing_status.csv")
                self.symbols = set(df[df['assetType'] == 'Stock']['symbol'].values)
                self.last_update = current_time
                logging.info(f"Updated stock symbols. Total count: {len(self.symbols)}")
            except Exception as e:
                logging.error(f"Failed to retrieve stock symbols: {e}")
                if not self.symbols:
                    raise
        return self.symbols
    
    def grab_data(self):
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)

        with open("data/dictionary.txt", "r") as file:
            words = [line.strip() for line in file]
            file.close()

        stock_symbols = self.get_stock_symbols()

        with open("data/symbols_data.txt", "a") as file:
            for item in stock_symbols:
                try:
                    if item in stock_symbols:
                        continue
                    if item.lower() in words:
                        file.write(f"${item} \n")
                    else:
                        file.write(f" {item} \n")
                except Exception as e:
                    logging.error(f"Couldn't process item {item}: {e}")

        logging.info(f"Symbols saved successfully: symbols_data.txt")