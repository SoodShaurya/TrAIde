from nltk.corpus import words
import configparser
import pandas as pd
from src.stock_manager import StockManager

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config

config = load_config()

df = pd.read_csv("data/listing_status.csv")
stock_symbols = set(df[df['assetType'] == 'Stock']['symbol'].values)

with open("data/symbols_data.txt", "w") as file:
    for item in stock_symbols:
        if item in words.words():
            file.write(f"${item}\n")
        else:
            file.write(f"{item}\n")