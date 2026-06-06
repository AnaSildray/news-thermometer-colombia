import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './NewsCards.css';

function NewsCards({ articles }) {
  const [expandedId, setExpandedId] = useState(null);

  const getSentimentColor = (sentiment) => {
    if (sentiment === 'positive') return '#10b981';
    if (sentiment === 'negative') return '#ef4444';
    return '#f59e0b';
  };

  const getSentimentEmoji = (sentiment) => {
    if (sentiment === 'positive') return '😊';
    if (sentiment === 'negative') return '😞';
    return '😐';
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 }
    }
  };

  return (
    <motion.div
      className="news-cards-container"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h3 className="news-title">📰 Noticias Analizadas ({articles.length})</h3>

      <motion.div className="news-grid">
        <AnimatePresence>
          {articles.map((article, idx) => (
            <motion.div
              key={idx}
              className="news-card"
              variants={itemVariants}
              layout
            >
              <div className="news-card-header">
                <div className="news-source-badge">{article.source}</div>
                <div className="news-sentiment-badge">
                  <span className="sentiment-emoji">
                    {getSentimentEmoji(
                      Object.keys(article.sentiment_distribution).reduce((a, b) =>
                        article.sentiment_distribution[a] > article.sentiment_distribution[b] ? a : b
                      )
                    )}
                  </span>
                </div>
              </div>

              <h4 className="news-title-text">{article.title}</h4>

              <div className="news-stats">
                <div className="stat">
                  <span className="stat-emoji">😊</span>
                  <span className="stat-label">Positivos:</span>
                  <span className="stat-value">{article.sentiment_distribution.positive}</span>
                </div>
                <div className="stat">
                  <span className="stat-emoji">😞</span>
                  <span className="stat-label">Negativos:</span>
                  <span className="stat-value">{article.sentiment_distribution.negative}</span>
                </div>
                <div className="stat">
                  <span className="stat-emoji">😐</span>
                  <span className="stat-label">Neutrales:</span>
                  <span className="stat-value">{article.sentiment_distribution.neutral}</span>
                </div>
              </div>

              <button
                className="expand-button"
                onClick={() => setExpandedId(expandedId === idx ? null : idx)}
              >
                {expandedId === idx ? 'Ver menos' : 'Ver comentarios'} ({article.comments.length})
              </button>

              <AnimatePresence>
                {expandedId === idx && (
                  <motion.div
                    className="comments-section"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="comments-list">
                      {article.comments.map((comment, cIdx) => (
                        <motion.div
                          key={cIdx}
                          className="comment-item"
                          style={{
                            borderLeftColor: getSentimentColor(comment.sentiment)
                          }}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: cIdx * 0.05 }}
                        >
                          <span className="comment-sentiment">
                            {getSentimentEmoji(comment.sentiment)}
                          </span>
                          <p className="comment-text">{comment.text}</p>
                          <span className="comment-label">{comment.sentiment}</span>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}

export default NewsCards;
