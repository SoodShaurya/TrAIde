# src/data_processor.py
import pandas as pd
from typing import List
import logging

class DataProcessor:
    @staticmethod
    def generate_report(df: pd.DataFrame, timeframes: List[int]) -> pd.DataFrame:
        """Generate sentiment report for specified timeframes"""
        all_data = []
        
        for timeframe in timeframes:
            try:
                # Filter data for timeframe
                cutoff = pd.Timestamp.now() - pd.Timedelta(days=timeframe)
                timeframe_data = df[df['timestamp'] > cutoff]
                
                if not timeframe_data.empty:
                    # Calculate metrics
                    metrics = timeframe_data.groupby('symbol').agg({
                        'sentiment': ['mean', 'count', lambda x: (x > 0).mean()],
                        'score': 'sum'
                    })
                    
                    metrics.columns = ['avg_sentiment', 'mention_count', 'bullish_ratio', 'total_score']
                    metrics['timeframe_days'] = timeframe
                    all_data.append(metrics.reset_index())
                
            except Exception as e:
                logging.error(f"Error processing timeframe {timeframe}: {e}")
                continue
                
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
