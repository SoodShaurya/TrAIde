# src/sentiment_analyzer.py
import logging

from transformers import pipeline
from sentence_transformers import SentenceTransformer
from typing import Dict

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
            top_k=None,
            truncation=True,
            max_length=4096
        )
        
    def analyze_text(self, text: str) -> Dict:
        try:
            results = self.analyzer(text)[0]
            sentiment_scores = {
                'positive_score': 0,
                'neutral_score': 0,
                'negative_score': 0,
                'compound_score': 0
            }
            
            for result in results:
                if result['label'] == 'positive':
                    sentiment_scores['positive_score'] = result['score']
                elif result['label'] == 'negative':
                    sentiment_scores['negative_score'] = result['score']
                else:
                    sentiment_scores['neutral_score'] = result['score']
            
            sentiment_scores['compound_score'] = (
                sentiment_scores['positive_score'] - 
                sentiment_scores['negative_score']
            )
            
            return sentiment_scores
            
        except Exception as e:
            logging.error(f"Sentiment analysis failed: {e}")
            return {
                'positive_score': 0,
                'neutral_score': 0,
                'negative_score': 0,
                'compound_score': 0
            }