from datetime import datetime, timedelta

from utils.mongo import initialize_mongodb
from utils.logger import setup_logger

class API:
    def __init__(self):
        setup_logger()
        self.collection = initialize_mongodb()

    def get_ticker(self, ticker):
        """Get all documents mentioning a specific ticker. Sorts by timestamp ASC."""
        aggregation = self.collection.aggregate([
            {
                '$match': {
                    'tickers': ticker
                }
            },
            {
                '$sort': {
                    'timestamp': 1
                }
            }
        ])
        return aggregation
    
    def sort_alltime_upvotes(self):
        """Sorts all tickers by all time upvotes."""
        aggregation = self.collection.aggregate([
            {
                '$group': {
                    '_id': '$tickers', 
                    'total_upvotes': {
                        '$sum': '$upvotes'
                    }
                }
            }, {
                '$sort': {
                    'total_upvotes': -1
                }
            }
        ])
        items = []
        for item in list(aggregation):
            if len(item['_id']) == 1:
                items.append(item)
            
        return items
    
    def sort_daily_upvotes(self):
        """Sorts all tickers by daily upvotes."""
        aggregation = self.collection.aggregate([
            {
                '$match': {
                    'timestamp': {
                        '$gte': datetime.timestamp(datetime.now() - timedelta(days=1))
                    }
                }
            }, 
            {
                '$group': {
                    '_id': '$tickers', 
                    'total_upvotes': {
                        '$sum': '$upvotes'
                    }
                }
            }, 
            {
                '$sort': {
                    'total_upvotes': -1
                }
            }
        ])
        items = []
        for item in list(aggregation):
            if len(item['_id']) == 1:
                items.append(item)
            
        return items