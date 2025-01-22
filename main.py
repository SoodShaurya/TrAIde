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

HOST = "127.0.0.1"
PORT = 8027

def setup():
    setup_logger()
    config = load_config()
    collection = initialize_mongodb(config["MONGODB"]["port"])
    stock_manager = StockManager(config)
    return API(collection), config, collection, stock_manager

async def stream_data(config, collection):
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

async def retrieve_symbols(stock_manager: StockManager):
    while True:
        try:
            await asyncio.sleep(stock_manager.update_interval)
            logging.info("Updating stock data...")
            stock_manager.grab_data()
        except Exception as e:
            logging.error(f"Error in retrieve_symbols: {e}")
            await asyncio.sleep(60)  # Retry after 60 seconds if an error occurs

async def run_server(app):
    try:
        config = uvicorn.Config(app(), host=HOST, port=PORT, reload=True)
        server = uvicorn.Server(config)
        logging.info(f"Starting API server...: {HOST+':'+str(PORT)}")
        await server.serve()
    except Exception as e:
        logging.error(f"API server failed: {e}")
        raise

async def main():
    try:
        app, config, collection, stock_manager = setup()
        await asyncio.gather(
            run_server(app),
            stream_data(config, collection),
            retrieve_symbols(stock_manager)  # Run the symbols update loop
        )
    except Exception as e:
        logging.critical(f"Main execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())