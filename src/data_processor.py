import pandas as pd
from typing import List
import logging

class DataProcessor:
    @staticmethod
    def weighted_sentiment(timeframe_data: pd.DataFrame) -> float:
        """Calculate custom weighted average sentiment based on score."""
        max_score = max(timeframe_data['score'])

        norm_scores = timeframe_data['score'] / max_score
        
        alpha = 0.5
        beta = 0.5

        weighted_sentiment = norm_scores * alpha + timeframe_data['sentiment'] * beta

        return weighted_sentiment

    @staticmethod
    def generate_report(df: pd.DataFrame, days: int = 0, hours: int = 0) -> pd.DataFrame:
        """Generate sentiment report for specified timeframes."""
        all_data = []
        
        try:
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=days, hours=hours)
            timeframe_data = df[df['timestamp'] > cutoff]
            
            if not timeframe_data.empty:
                weighted_sentiment_value = DataProcessor.weighted_sentiment(timeframe_data)
                mention_count = timeframe_data.groupby('symbol').size()
                bullish_ratio = (timeframe_data['sentiment'] > 0).mean()
                total_score = timeframe_data.groupby('symbol')['score'].sum()

                metrics = pd.DataFrame({
                    'weighted_sentiment': weighted_sentiment_value,
                    'mention_count': mention_count,
                    'bullish_ratio': bullish_ratio,
                    'total_score': total_score,
                    'timeframe_days': days
                }).reset_index()

                all_data.append(metrics)
            
        except Exception as e:
            logging.error(f"Error processing timeframe {days} days and {hours} hours: {e}")
                
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()