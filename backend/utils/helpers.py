"""Helper functions for the application"""

import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    return text.strip()

def calculate_sentiment_score(positive: int, negative: int, neutral: int) -> int:
    """Calculate overall sentiment score (0-100)"""
    total = positive + negative + neutral
    
    if total == 0:
        return 50
    
    # Score: 50 is neutral, 100 is most positive, 0 is most negative
    positive_ratio = positive / total
    negative_ratio = negative / total
    
    score = 50 + (positive_ratio - negative_ratio) * 50
    score = max(0, min(100, int(score)))
    
    return score

def get_sentiment_level(score: int) -> str:
    """Get sentiment level from score"""
    if score >= 67:
        return 'positive'
    elif score >= 34:
        return 'neutral'
    else:
        return 'negative'

def format_timestamp(dt: datetime = None) -> str:
    """Format datetime to ISO string"""
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()

def safe_json_loads(json_str: str, default=None):
    """Safely load JSON string"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def retry_on_exception(func, retries=3, delay=1):
    """Retry a function with exponential backoff"""
    import time
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            if attempt == retries - 1:
                raise
            wait_time = delay * (2 ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
            time.sleep(wait_time)
