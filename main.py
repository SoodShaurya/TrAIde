# main.py
import configparser
from src.stock_manager import StockManager
from src.reddit_scraper import RedditScraper
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_processor import DataProcessor
from config.__init__ import load_config
from pymongo import MongoClient
from utils.logger import setup_logger
from src.timers import Timer

import logging
import os
import pandas as pd
from datetime import datetime
import os
from src.data_grabber import grab_data

def initialize_mongodb():
    # Initialize MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your connection string
    db = client["global"]  # Database name
    collection = db["posts"]  # Collection name
    return collection

def main():
    setup_logger()
    try:
        # Load configuration
        config = load_config()
        
        # Initialize components
        with open("data/symbols_data.txt", "r") as file:
            stock_symbols = {line.strip() for line in file}
            file.close()
        

        reddit_scraper = RedditScraper(dict(config['REDDIT']), stock_symbols, collection)
        sentiment_analyzer = SentimentAnalyzer()
        data_processor = DataProcessor()
        timer = Timer()
        
        # Process data for different timeframes
        timeframes = [1]
        timer.start("Getting submissions from Reddit.")
        submissions = reddit_scraper.get_submissions(max(timeframes))
        timer.end()
        timer.get_elapsed_time(f"Got {len(submissions)} submissions in %m seconds.")
        
        # Analyze sentiments
        timer.start(f"Processing {len(submissions)} submissions.")
        sentiment_data = sentiment_analyzer.process_submissions(submissions)
        timer.end()
        timer.get_elapsed_time(f"Processed {len(submissions)} submissions in %m seconds")
        
        # Generate report
        timer.start("Generating report.")
        report = data_processor.generate_report(sentiment_data, timeframes)
        timer.end()
        timer.get_elapsed_time("Generated report in %m seconds.")
        
        # Save report
        timestamp = datetime.now()
        report_dir = 'reports'
        os.makedirs(report_dir, exist_ok=True)
        report.to_csv(f'reports/sentiment_report_{timestamp}.csv', index=False)
        logging.info(f"Report generated successfully: sentiment_report_{timestamp}.csv")
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        raise

if __name__ == "__main__":
    collection = initialize_mongodb()
    print("MongoDB initialized and collection ready.")
    main()