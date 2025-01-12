# main.py
import logging

from src.reddit_scraper import RedditScraper
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_processor import DataProcessor
from src.data_grabber import grab_data
from config.__init__ import load_config
from utils.logger import setup_logger
from utils.timers import Timer

from utils.mongo import initialize_mongodb

# main.py
def main():
    setup_logger()
    try:
        config = load_config()
        
        # Initialize 
        collection = initialize_mongodb()
        with open("data/symbols_data.txt", "r") as file:
            stock_symbols = {line.strip() for line in file}
        
        sentiment_analyzer = SentimentAnalyzer()
        data_processor = DataProcessor(sentiment_analyzer, collection)
        reddit_scraper = RedditScraper(
            dict(config['REDDIT']), 
            stock_symbols,
            data_processor
        )

        logging.info("Starting Reddit stream...")
        reddit_scraper.stream_content()
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
