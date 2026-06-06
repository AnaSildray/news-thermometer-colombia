"""
Database utilities for storing sentiment analysis results
Uses SQLite by default
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class Database:
    """Database manager for sentiment analysis data"""
    
    def __init__(self, db_type: str = 'sqlite', db_path: str = 'sentiment_analysis.db'):
        """Initialize database connection"""
        self.db_type = db_type
        self.db_path = db_path
        self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self._create_tables()
            logger.info(f"SQLite database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing SQLite: {str(e)}")
    
    def _create_tables(self):
        """Create necessary tables"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                date DATE,
                sentiment_score INTEGER,
                overall_sentiment TEXT,
                positive_count INTEGER,
                negative_count INTEGER,
                neutral_count INTEGER,
                total_comments INTEGER,
                articles_count INTEGER,
                data JSON
            )
        ''')
        
        self.conn.commit()
        logger.info("Database tables created successfully")
    
    def save_analysis(self, analysis_data: Dict) -> int:
        """Save sentiment analysis results"""
        try:
            cursor = self.conn.cursor()
            timestamp = analysis_data.get('timestamp', datetime.now().isoformat())
            date = timestamp.split('T')[0]
            
            cursor.execute('''
                INSERT INTO analysis_results 
                (timestamp, date, sentiment_score, overall_sentiment, 
                 positive_count, negative_count, neutral_count, 
                 total_comments, articles_count, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                date,
                analysis_data.get('sentiment_score', 50),
                analysis_data.get('overall_sentiment', 'neutral'),
                analysis_data.get('sentiment_counts', {}).get('positive', 0),
                analysis_data.get('sentiment_counts', {}).get('negative', 0),
                analysis_data.get('sentiment_counts', {}).get('neutral', 0),
                analysis_data.get('total_comments', 0),
                analysis_data.get('articles_count', 0),
                json.dumps(analysis_data)
            ))
            
            self.conn.commit()
            analysis_id = cursor.lastrowid
            logger.info(f"Analysis saved with ID: {analysis_id}")
            return analysis_id
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            return None
    
    def get_analysis_history(self, limit: int = 30) -> List[Dict]:
        """Get historical sentiment analysis data"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM analysis_results
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row['id'],
                    'timestamp': row['timestamp'],
                    'date': row['date'],
                    'sentiment_score': row['sentiment_score'],
                    'overall_sentiment': row['overall_sentiment'],
                    'positive_count': row['positive_count'],
                    'negative_count': row['negative_count'],
                    'neutral_count': row['neutral_count'],
                    'total_comments': row['total_comments'],
                    'articles_count': row['articles_count']
                })
            return results
        except Exception as e:
            logger.error(f"Error retrieving history: {str(e)}")
            return []
    
    def get_today_analysis(self) -> Optional[Dict]:
        """Get today's sentiment analysis"""
        try:
            cursor = self.conn.cursor()
            today = datetime.now().date()
            cursor.execute('''
                SELECT * FROM analysis_results
                WHERE date = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (today,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'timestamp': row['timestamp'],
                    'date': row['date'],
                    'sentiment_score': row['sentiment_score'],
                    'overall_sentiment': row['overall_sentiment'],
                    'positive_count': row['positive_count'],
                    'negative_count': row['negative_count'],
                    'neutral_count': row['neutral_count'],
                    'total_comments': row['total_comments'],
                    'articles_count': row['articles_count']
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving today's analysis: {str(e)}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
