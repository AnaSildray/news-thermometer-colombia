"""Flask configuration and initialization"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # Database
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'sentiment_analysis.db')
    
    # Sentiment
    SENTIMENT_MODEL = os.getenv('SENTIMENT_MODEL', 'simple')
    
    # Scraper
    SCRAPER_TIMEOUT = int(os.getenv('SCRAPER_TIMEOUT', 10))
    SCRAPER_RETRIES = int(os.getenv('SCRAPER_RETRIES', 3))
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
