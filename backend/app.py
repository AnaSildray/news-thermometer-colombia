"""
Main Flask application for News Thermometer Colombia
Handles API endpoints for scraping, sentiment analysis, and data retrieval
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

from config import config
from scraper.news_scraper import NewsScraper
from sentiment.analyzer import SentimentAnalyzer
from utils.database import Database

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])
CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
try:
    scraper = NewsScraper(
        timeout=app.config.get('SCRAPER_TIMEOUT'),
        retries=app.config.get('SCRAPER_RETRIES')
    )
    sentiment_analyzer = SentimentAnalyzer(
        model_name=app.config.get('SENTIMENT_MODEL')
    )
    db = Database(
        db_type=app.config.get('DATABASE_TYPE'),
        db_path=app.config.get('DATABASE_PATH')
    )
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {str(e)}")

# ==================== Routes ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    """
    Main endpoint to scrape news and analyze sentiment
    
    Returns:
    - overall_sentiment: positive, negative, neutral
    - sentiment_score: 0-100 (100 = most positive)
    - breakdown: count of positive, negative, neutral comments
    - articles: scraped articles with sentiment analysis
    - thermometer_level: 0-100 for thermometer visualization
    """
    try:
        # Get parameters
        limit = request.args.get('limit', default=5, type=int)
        
        logger.info(f"Starting analysis with limit={limit}")
        
        # Scrape news
        articles = scraper.scrape_all(limit=limit)
        
        if not articles:
            return jsonify({
                'error': 'No news articles found',
                'timestamp': datetime.now().isoformat()
            }), 404
        
        # Analyze sentiment for each article
        analyzed_articles = []
        total_comments = 0
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for article in articles:
            comments = article.get('comments', [])
            article_sentiments = []
            
            for comment in comments:
                sentiment = sentiment_analyzer.analyze(comment)
                article_sentiments.append({
                    'text': comment,
                    'sentiment': sentiment
                })
                sentiment_counts[sentiment] += 1
                total_comments += 1
            
            analyzed_articles.append({
                'title': article.get('title'),
                'url': article.get('url'),
                'source': article.get('source'),
                'published_at': article.get('published_at'),
                'comments': article_sentiments,
                'sentiment_distribution': {
                    'positive': sum(1 for s in article_sentiments if s['sentiment'] == 'positive'),
                    'negative': sum(1 for s in article_sentiments if s['sentiment'] == 'negative'),
                    'neutral': sum(1 for s in article_sentiments if s['sentiment'] == 'neutral')
                }
            })
        
        # Calculate overall sentiment
        if total_comments == 0:
            sentiment_score = 50
            overall_sentiment = 'neutral'
        else:
            positive_ratio = sentiment_counts['positive'] / total_comments
            negative_ratio = sentiment_counts['negative'] / total_comments
            
            # Score: 0-100 where 50 is neutral
            sentiment_score = int(50 + (positive_ratio - negative_ratio) * 50)
            sentiment_score = max(0, min(100, sentiment_score))  # Clamp between 0-100
            
            if sentiment_score >= 67:
                overall_sentiment = 'positive'
            elif sentiment_score <= 33:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
        
        # Determine thermometer level and color
        if sentiment_score >= 67:
            thermometer_color = 'green'
        elif sentiment_score >= 34:
            thermometer_color = 'yellow'
        else:
            thermometer_color = 'red'
        
        # Save to database
        db.save_analysis({
            'timestamp': datetime.now().isoformat(),
            'sentiment_score': sentiment_score,
            'overall_sentiment': overall_sentiment,
            'sentiment_counts': sentiment_counts,
            'total_comments': total_comments,
            'articles_count': len(analyzed_articles)
        })
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'overall_sentiment': overall_sentiment,
            'sentiment_score': sentiment_score,
            'thermometer_level': sentiment_score,
            'thermometer_color': thermometer_color,
            'breakdown': {
                'positive': sentiment_counts['positive'],
                'negative': sentiment_counts['negative'],
                'neutral': sentiment_counts['neutral'],
                'total': total_comments
            },
            'percentage': {
                'positive': round((sentiment_counts['positive'] / total_comments * 100), 2) if total_comments > 0 else 0,
                'negative': round((sentiment_counts['negative'] / total_comments * 100), 2) if total_comments > 0 else 0,
                'neutral': round((sentiment_counts['neutral'] / total_comments * 100), 2) if total_comments > 0 else 0
            },
            'articles_analyzed': len(analyzed_articles),
            'articles': analyzed_articles
        }), 200
    
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get historical sentiment analysis"""
    try:
        limit = request.args.get('limit', default=30, type=int)
        history = db.get_analysis_history(limit=limit)
        
        return jsonify({
            'success': True,
            'data': history,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/today', methods=['GET'])
def get_today_analysis():
    """Get today's sentiment analysis"""
    try:
        today_data = db.get_today_analysis()
        
        if not today_data:
            return jsonify({
                'error': 'No analysis data for today',
                'timestamp': datetime.now().isoformat()
            }), 404
        
        return jsonify({
            'success': True,
            'data': today_data,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving today's analysis: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Get list of available news sources"""
    try:
        sources = scraper.get_available_sources()
        return jsonify({
            'success': True,
            'sources': sources,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving sources: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== Main ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', False)
    app.run(host='0.0.0.0', port=port, debug=debug)
