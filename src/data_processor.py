# src/data_processor.py
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime

class DataProcessor:
    def __init__(self, sentiment_analyzer, mongodb_collection):
        self.sentiment_analyzer = sentiment_analyzer
        self.collection = mongodb_collection
        
    def process_item(self, item_data: Dict):
        try:
            # Analyze sentiment
            sentiment_scores = self.sentiment_analyzer.analyze_text(item_data['content'])
            
            # Enrich the document
            item_data['sentiment_scores'] = sentiment_scores
            item_data['compound_score'] = sentiment_scores['compound_score']
            
            # Console output
            logging.info(f"\nNew {item_data['type']} processed:")
            logging.info(f"Content: {item_data['content'][:200]}...")
            logging.info(f"Tickers: {item_data['tickers']}")
            logging.info(f"Sentiment: {sentiment_scores}")
            
            # Store in MongoDB
            self.collection.insert_one(item_data)
            
        except Exception as e:
            logging.error(f"Error processing {item_data['type']}: {e}")
