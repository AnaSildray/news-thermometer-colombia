"""
Sentiment analysis for Spanish language comments
Uses TextBlob for robust classification
"""

import logging
from typing import Literal
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Analyze sentiment of Spanish text comments"""
    
    def __init__(self, model_name: str = 'simple'):
        """Initialize sentiment analyzer"""
        self.model_name = model_name
        self._init_textblob()
    
    def _init_textblob(self):
        """Initialize TextBlob for sentiment analysis"""
        try:
            from textblob import TextBlob
            self.analyzer = TextBlob
            logger.info("TextBlob sentiment analyzer initialized")
        except Exception as e:
            logger.error(f"Error initializing TextBlob: {str(e)}")
            self.analyzer = None
    
    def analyze(self, text: str) -> Literal['positive', 'negative', 'neutral']:
        """Analyze sentiment of a text"""
        if not text or len(text.strip()) == 0:
            return 'neutral'
        
        try:
            return self._analyze_textblob(text)
        except Exception as e:
            logger.warning(f"Error analyzing sentiment: {str(e)}")
            return 'neutral'
    
    def _analyze_textblob(self, text: str) -> Literal['positive', 'negative', 'neutral']:
        """Analyze using TextBlob"""
        try:
            blob = self.analyzer(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            logger.warning(f"TextBlob analysis failed: {str(e)}")
            return 'neutral'
    
    def analyze_batch(self, texts: list) -> dict:
        """Analyze sentiment of multiple texts"""
        sentiments = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        for text in texts:
            sentiment = self.analyze(text)
            sentiments[sentiment] += 1
        
        return sentiments
