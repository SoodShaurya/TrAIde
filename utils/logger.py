import os
import logging
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Setup logging configuration
    log_file = f'logs/sentiment_analysis_{datetime.now():%Y%m%d}.log'
    filehandler = logging.FileHandler(log_file)
    streamhandler = logging.StreamHandler()
    logging.basicConfig(
        handlers=[filehandler, streamhandler],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
