# main.py
import logging

from config.__init__ import load_config

from src.reddit_scraper import RedditScraper
from src.models import SentimentAnalyzer
from src.data_processor import DataProcessor
from src.data_grabber import grab_data

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
        
        sentiment_analyzer = SentimentAnalyzer()
        data_processor = DataProcessor(sentiment_analyzer, collection)
        reddit_scraper = RedditScraper(
            dict(config['REDDIT']),
            data_processor
        )

        # timer = Timer()

        # timer.start()
        # reddit_scraper.fetch_posts(10000)
        # timer.stop()
        # timer.get_elapsed_time("Time to fetch posts: %m seconds")

        logging.info("Starting Reddit stream...")
        reddit_scraper.stream_content()
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        raise

if __name__ == "__main__":
    main()