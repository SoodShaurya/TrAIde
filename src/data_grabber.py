import configparser
import pandas as pd
import logging
from src.stock_manager import StockManager
import nltk
import os
from config.__init__ import load_config


def grab_data():
    config = load_config()

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    stock_manager = StockManager(config['ALPHA_VANTAGE']['api_key'])
    stock_symbols = stock_manager.get_stock_symbols()

    with open("data/symbols_data.txt", "w+") as file:
        for item in stock_symbols:
            try:
                if item.lower() in nltk.corpus.words.words():
                    file.write(f"${item}\n")
                    print(f"${item}")
                else:
                    file.write(f"{item}\n")
                    print(f"{item}")
            except Exception as e:
                logging.error(f"Error when grabbing stock symbols: {e}")
                if Exception == LookupError:
                    logging.error("Couldn't find words corpus.")
                    nltk.download("words")

    logging.info(f"Symbols saved successfully: symbols_data.txt")