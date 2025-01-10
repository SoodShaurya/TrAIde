# src/reddit_scraper.py
import praw
from datetime import datetime, timedelta
from typing import List, Dict
import logging

class RedditScraper:
    def __init__(self, reddit_config: dict, stock_symbols: set):
        self.reddit = praw.Reddit(
            client_id=reddit_config['client_id'],
            client_secret=reddit_config['client_secret'],
            user_agent=reddit_config['user_agent']
        )
        self.stock_symbols = stock_symbols
        self.subreddits = reddit_config['subreddits'].split(',')

    def extract_stock_mentions(self, text: str) -> List[str]:
        """Extract valid stock symbols from text"""
        words = text.upper().split()
        return [word for word in words if word in self.stock_symbols]

    def get_submissions(self, timeframe: int) -> List[Dict]:
        """Scrape Reddit submissions and comments within timeframe"""
        submissions_data = []
        start_time = datetime.utcnow() - timedelta(days=timeframe)

        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                for submission in subreddit.new(limit=None):
                    if datetime.utcfromtimestamp(submission.created_utc) < start_time:
                        break

                    # Process submission
                    content = f"{submission.title} {submission.selftext}"
                    stock_mentions = self.extract_stock_mentions(content)
                    if stock_mentions:
                        submissions_data.append({
                            'symbols': stock_mentions,
                            'content': content,
                            'timestamp': datetime.utcfromtimestamp(submission.created_utc),
                            'score': submission.score,
                            'type': 'submission',
                            'subreddit': subreddit_name
                        })

                    # Process comments
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        stock_mentions = self.extract_stock_mentions(comment.body)
                        if stock_mentions:
                            submissions_data.append({
                                'symbols': stock_mentions,
                                'content': comment.body,
                                'timestamp': datetime.utcfromtimestamp(comment.created_utc),
                                'score': comment.score,
                                'type': 'comment',
                                'subreddit': subreddit_name
                            })

            except Exception as e:
                logging.error(f"Error processing subreddit {subreddit_name}: {e}")
                continue

        return submissions_data
