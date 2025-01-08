import configparser
import pandas as pd
import logging
from src.stock_manager import StockManager
from nltk.corpus import words
import os

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config

def grab_data():
    config = load_config()

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    stock_manager = StockManager(config['ALPHA_VANTAGE']['api_key'])
    stock_symbols = stock_manager.get_stock_symbols()

    with open("data/symbols_data.txt", "w") as file:
        for item in stock_symbols:
            if item in words.words():
                file.write(f"${item}\n")
            else:
                file.write(f"{item}\n")

    logging.info(f"Symbols saved successfully: symbols_data.txt")