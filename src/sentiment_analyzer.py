# src/sentiment_analyzer.py
from transformers import pipeline
from typing import Dict, List
import pandas as pd 
import logging

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
                            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
                            top_k=None,
                            truncation=True,
                            max_length=4096
                        )
        
    def get_compound_score(self, data):
        positive_score = 0
        negative_score = 0

        for entry in data:
            if entry['label'] == 'positive':
                positive_score = entry['score']
            elif entry['label'] == 'negative':
                negative_score = entry['score']

        sentiment_score = positive_score - negative_score
        
        return sentiment_score

    def analyze_text(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using distilbert"""
        try:
            return self.analyzer(text)[0]
        except Exception as e:
            logging.error(f"Sentiment analysis failed: {e}")
            return [{'label': 'positive', 'score': 0}, {'label': 'neutral', 'score': 0}, {'label': 'negative', 'score': 0}]

    def process_submissions(self, submissions: List[Dict]) -> pd.DataFrame:
        """Process submissions and generate sentiment analysis"""
        processed_data = []
        
        for submission in submissions:
            sentiment = self.analyze_text(submission['content'])
            for symbol in submission['symbols']:
                processed_data.append({
                    'symbol': symbol,
                    'timestamp': submission['timestamp'],
                    'sentiment': self.get_compound_score(sentiment),
                    'score': submission['score'],
                    'subreddit': submission['subreddit'],
                    'type': submission['type']
                })

        return pd.DataFrame(processed_data)