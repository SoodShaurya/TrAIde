import configparser
import pandas as pd
import logging
from src.stock_manager import StockManager
from nltk.corpus import words
import os

def load_config() -> configparser.ConfigParser:
    config_dir = 'config'
    config_file = os.path.join(config_dir, 'config.ini')
    template_file = os.path.join(config_dir, 'configtemplate.ini')
    os.makedirs(config_dir, exist_ok=True)
    if not os.path.exists(config_file):
        if os.path.exists(template_file):
            with open(template_file, 'r') as template:
                content = template.read()
            with open(config_file, 'w') as config:
                config.write(content)
            print(f"Created {config_file} from {template_file}.")
        else:
            raise FileNotFoundError(f"Template file {template_file} not found.")
    config = configparser.ConfigParser()
    config.read(config_file)
    print('config')
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