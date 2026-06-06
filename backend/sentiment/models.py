"""Pre-trained models for sentiment analysis"""

import logging

logger = logging.getLogger(__name__)

class SentimentModel:
    """Base class for sentiment models"""
    
    def __init__(self, name: str):
        self.name = name
    
    def predict(self, text: str) -> str:
        raise NotImplementedError

class TextBlobModel(SentimentModel):
    """TextBlob-based sentiment model"""
    
    def __init__(self):
        super().__init__('textblob')
        try:
            from textblob import TextBlob
            self.TextBlob = TextBlob
            logger.info("TextBlob model loaded successfully")
        except ImportError:
            logger.error("TextBlob not installed")
            self.TextBlob = None
    
    def predict(self, text: str) -> str:
        if not self.TextBlob:
            return 'neutral'
        
        try:
            blob = self.TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            logger.warning(f"Error in TextBlob prediction: {e}")
            return 'neutral'

class TransformerModel(SentimentModel):
    """Transformer-based sentiment model"""
    
    def __init__(self):
        super().__init__('transformer')
        try:
            from transformers import pipeline
            self.pipeline = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                device=-1
            )
            logger.info("Transformer model loaded successfully")
        except ImportError:
            logger.error("Transformers not installed")
            self.pipeline = None
    
    def predict(self, text: str) -> str:
        if not self.pipeline:
            return 'neutral'
        
        try:
            result = self.pipeline(text[:512])
            if result:
                label = result[0]['label'].lower()
                if label in ['5 stars', 'positive']:
                    return 'positive'
                elif label in ['1 star', 'negative']:
                    return 'negative'
            return 'neutral'
        except Exception as e:
            logger.warning(f"Error in Transformer prediction: {e}")
            return 'neutral'
