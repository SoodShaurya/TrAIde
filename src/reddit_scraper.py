# src/reddit_scraper.py
import praw
import logging
import time

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class RedditScraper:
    def __init__(self, reddit_config: dict, data_processor):
        self.reddit = praw.Reddit(
            client_id=reddit_config['client_id'],
            client_secret=reddit_config['client_secret'],
            user_agent=reddit_config['user_agent']
        )
        with open("data/symbols_data.txt", "r") as file:
            self.stock_symbols = {line.strip() for line in file}
            file.close()
        self.subreddits = reddit_config['subreddits'].split(',')
        self.data_processor = data_processor
        self.executor = ThreadPoolExecutor(max_workers=2)

    def extract_symbol_mentions(self, text: str):
        words = text.split()
        return [word for word in words if word in self.stock_symbols]

    def process_submission(self, submission):
        content = f"{submission.title} {submission.selftext}"
        stock_mentions = self.extract_symbol_mentions(content)
        if stock_mentions:
            document = {
                '_id': submission.id,
                'post_id': submission.id,
                'type': 'post',
                'tickers': stock_mentions,
                'title': submission.title,
                'content': submission.selftext,
                'author': submission.author.name if submission.author else None,
                'subreddit': submission.subreddit.display_name,
                'upvotes': submission.score,
                'timestamp': int(submission.created_utc),
                'url': f"https://reddit.com{submission.permalink}",
                'scraped_at': datetime.utcnow().isoformat()
            }
            self.data_processor.process_item(document)

    def process_comment(self, comment):
        stock_mentions = self.extract_symbol_mentions(comment.body)
        if stock_mentions:
            document = {
                '_id': comment.id,
                'post_id': comment.link_id.split('_')[1],
                'type': 'comment',
                'tickers': stock_mentions,
                'content': comment.body,
                'author': comment.author.name if comment.author else None,
                'subreddit': comment.subreddit.display_name,
                'upvotes': comment.score,
                'timestamp': int(comment.created_utc),
                'url': f"https://reddit.com{comment.permalink}",
                'scraped_at': datetime.utcnow().isoformat()
            }
            self.data_processor.process_item(document)

    def stream_submissions(self, subreddit):
        try:
            for submission in subreddit.stream.submissions(skip_existing=False):
                if self.data_processor.item_exists(submission.id):
                    logging.info(f"Skipping post {submission.id}")
                else:
                    self.process_submission(submission)
        except Exception as e:
            logging.error(f"Error streaming submissions: {e}")

    def stream_comments(self, subreddit):
        try:
            for comment in subreddit.stream.comments(skip_existing=False):
                if self.data_processor.item_exists(comment.id):
                    logging.info(f"Skipping comment {comment.id}")
                else:     
                    self.process_comment(comment)
        except Exception as e:
            logging.error(f"Error streaming comments: {e}")

    def stream_content(self):
        """Stream both submissions and comments concurrently"""
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Start submission and comment streams in separate threads
                self.executor.submit(self.stream_submissions, subreddit)
                self.executor.submit(self.stream_comments, subreddit)
                
                logging.info(f"Started streaming from r/{subreddit_name}")
                
            except Exception as e:
                logging.error(f"Error setting up stream for subreddit {subreddit_name}: {e}")
                continue

    def fetch_posts(self, n):
        """Retrospectively retrieve n posts and the comments on each post"""
        for subreddit_name in self.subreddits:
            subreddit = self.reddit.subreddit(subreddit_name)
            try:
                for submission in subreddit.new(limit=n):
                    if self.data_processor.item_exists(submission.id):
                        logging.info(f"Skipping post {submission.id}")
                        continue
                    self.process_submission(submission)
                    submission.comments.replace_more(limit=100)
                    for comment in submission.comments.list():
                        if self.data_processor.item_exists(comment.id):
                            logging.info(f"Skipping comment {comment.id}")
                            continue
                        self.process_comment(comment)
            except Exception as e:
                logging.error(f"Error fetching posts from r/{subreddit_name}: {e}")
                time.sleep(60)