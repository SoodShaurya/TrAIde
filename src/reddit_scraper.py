# src/reddit_scraper.py
import praw
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import praw
from datetime import datetime
import logging
from pymongo import MongoClient


class RedditScraper:
    def __init__(self, reddit_config: dict, stock_symbols: set, collection):
        self.reddit = praw.Reddit(
            client_id=reddit_config['client_id'],
            client_secret=reddit_config['client_secret'],
            user_agent=reddit_config['user_agent']
        )
        self.stock_symbols = stock_symbols
        self.subreddits = reddit_config['subreddits'].split(',')
        self.collection = collection

    def extract_symbol_mentions(self, text: str):
        """Extract valid stock symbols from text"""
        words = text.split()
        return [word for word in words if word in self.stock_symbols]

    def stream_to_mongodb(self):
        """Stream Reddit posts and comments to MongoDB"""
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)

                # Stream submissions (posts)
                for submission in subreddit.stream.submissions(skip_existing=False):
                    content = f"{submission.title} {submission.selftext}"
                    stock_mentions = self.extract_stock_mentions(content)
                    if stock_mentions:
                        document = {
                            '_id': submission.id,
                            'post_id': submission.id,
                            'type': 'post',
                            'tickers': stock_mentions,
                            'title': submission.title,
                            'content': submission.selftext,
                            'author': submission.author.name if submission.author else None,
                            'subreddit': subreddit_name,
                            'upvotes': submission.score,
                            'timestamp': datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                            'url': f"https://reddit.com{submission.permalink}",
                            'scraped_at': datetime.utcnow().isoformat()
                        }
                        self.collection.insert_one(document)

                # Stream comments
                for comment in subreddit.stream.comments(skip_existing=True):
                    stock_mentions = self.extract_stock_mentions(comment.body)
                    if stock_mentions:
                        document = {
                            '_id': comment.id,
                            'post_id': comment.link_id.split('_')[1],  # Extract post ID from link_id
                            'type': 'comment',
                            'tickers': stock_mentions,
                            'title': None,
                            'content': comment.body,
                            'author': comment.author.name if comment.author else None,
                            'subreddit': subreddit_name,
                            'upvotes': comment.score,
                            'timestamp': datetime.utcfromtimestamp(comment.created_utc).isoformat(),
                            'url': f"https://reddit.com{comment.permalink}",
                            'scraped_at': datetime.utcnow().isoformat()
                        }
                        self.collection.insert_one(document)

            except Exception as e:
                logging.error(f"Error streaming subreddit {subreddit_name}: {e}")
                continue
