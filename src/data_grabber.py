import configparser
import pandas as pd
import logging
from src.stock_manager import StockManager
import os

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config

def grab_data():
    config = load_config()

    data_dir = "data"
    os.mkdir(data_dir)

    stock_manager = StockManager(config['ALPHA_VANTAGE']['api_key'])
    stock_symbols = stock_manager.get_stock_symbols()

    stock_symbols.to_csv(f'{data_dir}/symbols.csv', index=False)
    logging.info(f"Report generated successfully: symbols_data.csv")