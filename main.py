# main.py
import configparser
from src.stock_manager import StockManager
from src.reddit_scraper import RedditScraper
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_processor import DataProcessor
from utils.logger import setup_logger
import logging
import os
import pandas as pd
from datetime import datetime
import os


def load_config() -> configparser.ConfigParser:
    """Load and validate configuration from config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    config.read(config_path)
    _validate_config(config)
    return config

def main():
    setup_logger()
    try:
        # Load configuration
        config = load_config()
        
        # Initialize components
        with open("data/symbols_data.txt", "r") as file:
            stock_symbols = {line.strip() for line in file}
        
        reddit_scraper = RedditScraper(dict(config['REDDIT']), stock_symbols)
        sentiment_analyzer = SentimentAnalyzer()
        data_processor = DataProcessor()
        
        # Process data for different timeframes
        timeframes = [1]
        submissions = reddit_scraper.get_submissions(max(timeframes))
        
        # Analyze sentiments
        sentiment_data = sentiment_analyzer.process_submissions(submissions)
        
        # Generate report
        report = data_processor.generate_report(sentiment_data, timeframes)
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_dir = 'reports'
        os.makedirs(report_dir, exist_ok=True)
        report.to_csv(f'reports/sentiment_report_{timestamp}.csv', index=False)
        logging.info(f"Report generated successfully: sentiment_report_{timestamp}.csv")
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
