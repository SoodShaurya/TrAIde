# src/sentiment_analyzer.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
import pandas as pd
import logging

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using VADER"""
        try:
            return self.analyzer.polarity_scores(text)
        except Exception as e:
            logging.error(f"Sentiment analysis failed: {e}")
            return {'compound': 0, 'pos': 0, 'neu': 0, 'neg': 0}

    def process_submissions(self, submissions: List[Dict]) -> pd.DataFrame:
        """Process submissions and generate sentiment analysis"""
        processed_data = []
        
        for submission in submissions:
            sentiment = self.analyze_text(submission['content'])
            for symbol in submission['symbols']:
                processed_data.append({
                    'symbol': symbol,
                    'timestamp': submission['timestamp'],
                    'sentiment': sentiment['compound'],
                    'score': submission['score'],
                    'subreddit': submission['subreddit'],
                    'type': submission['type']
                })

        return pd.DataFrame(processed_data)