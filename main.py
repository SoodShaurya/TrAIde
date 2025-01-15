# main.py
import logging
import uvicorn
import asyncio

from config.__init__ import load_config

from src.reddit_scraper import RedditScraper
from src.models import SentimentAnalyzer
from src.data_processor import DataProcessor
from src.stock_manager import StockManager
from src.api import API

from utils.logger import setup_logger
from utils.mongo import initialize_mongodb

def setup():
    """Initializes everything needed to run the api."""
    setup_logger()
    config = load_config()
    collection = initialize_mongodb()
    stock_manager = StockManager()
    return API(collection), config, collection, stock_manager

async def stream_data(config, collection):
    """Handles streaming data from Reddit and processing it."""
    try:
        sentiment_analyzer = SentimentAnalyzer()
        data_processor = DataProcessor(sentiment_analyzer, collection)
        reddit_scraper = RedditScraper(
            dict(config['REDDIT']),
            data_processor,
        )
        logging.info("Starting Reddit streaming...")
        reddit_scraper.stream_content()
    except Exception as e:
        logging.error(f"Streaming failed: {e}")
        raise

async def retrieve_symbols(stock_manager : StockManager):
    stock_manager.grab_data()
    asyncio.timeout(stock_manager.update_interval)

async def run_server(app):
    """Runs the FastAPI server."""
    try:
        config = uvicorn.Config(app(), host="127.0.0.1", port=8000, reload=True)
        server = uvicorn.Server(config)
        logging.info("Starting API server...")
        await server.serve()
    except Exception as e:
        logging.error(f"API server failed: {e}")
        raise

async def main():
    """Entry point for the application. Handles both the API server and data streaming."""
    try:
        app, config, collection, stock_manager = setup()
        await asyncio.gather(
            run_server(app),
            stream_data(config, collection),
            retrieve_symbols(stock_manager)
        )
    except Exception as e:
        logging.critical(f"Main execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())