import configparser
import pandas as pd
import logging
from src.stock_manager import StockManager
import os
from config.__init__ import load_config


def grab_data():
    config = load_config()

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    with open("data/dictionary.txt", "r") as file:
        words = [line.strip() for line in file]
        file.close()

    stock_manager = StockManager(config['ALPHA_VANTAGE']['api_key'])
    stock_symbols = stock_manager.get_stock_symbols()

    with open("data/symbols_data.txt", "w+") as file:
        for item in stock_symbols:
            try:
                if item.lower() in words:
                    file.write(f"${item} \n")
                else:
                    file.write(f" {item} \n")
            except Exception as e:
                logging.error(f"Couldn't process item {item}: {e}")

    logging.info(f"Symbols saved successfully: symbols_data.txt")