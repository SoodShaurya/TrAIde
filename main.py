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

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config

def main():
    setup_logger()
    try:
        # Load configuration
        config = load_config()
        
        # Initialize components
        stock_manager = StockManager(config['ALPHA_VANTAGE']['api_key'])
        stock_symbols = pd.read_csv("data/symbols_data.csv")
        
        reddit_scraper = RedditScraper(dict(config['REDDIT']), stock_symbols)
        sentiment_analyzer = SentimentAnalyzer()
        data_processor = DataProcessor()
        
        # Process data for different timeframes
        timeframes = [1]  # 1 day, 1 week, 1 month
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
