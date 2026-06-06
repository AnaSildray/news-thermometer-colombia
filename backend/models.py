"""Data models for sentiment analysis"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Comment:
    text: str
    sentiment: str
    source: str

@dataclass
class Article:
    title: str
    url: str
    source: str
    published_at: str
    comments: List[Comment]

@dataclass
class AnalysisResult:
    timestamp: datetime
    sentiment_score: int
    overall_sentiment: str
    positive_count: int
    negative_count: int
    neutral_count: int
    total_comments: int
    articles: List[Article]
