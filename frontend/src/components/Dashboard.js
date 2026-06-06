import React from 'react';
import { motion } from 'framer-motion';
import './Dashboard.css';

function Dashboard({ data }) {
  const stats = [
    {
      label: 'Comentarios Positivos',
      value: data.breakdown.positive,
      percentage: data.percentage.positive,
      color: '#10b981',
      emoji: '😊'
    },
    {
      label: 'Comentarios Negativos',
      value: data.breakdown.negative,
      percentage: data.percentage.negative,
      color: '#ef4444',
      emoji: '😞'
    },
    {
      label: 'Comentarios Neutrales',
      value: data.breakdown.neutral,
      percentage: data.percentage.neutral,
      color: '#f59e0b',
      emoji: '😐'
    },
    {
      label: 'Noticias Analizadas',
      value: data.articles_analyzed,
      percentage: 100,
      color: '#667eea',
      emoji: '📰'
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.1
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
      className="dashboard"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h3 className="dashboard-title">📊 Estadísticas Detalladas</h3>

      <motion.div className="stats-grid" variants={containerVariants}>
        {stats.map((stat, idx) => (
          <motion.div
            key={idx}
            className="stat-card"
            variants={itemVariants}
            style={{ borderTopColor: stat.color }}
          >
            <div className="stat-emoji">{stat.emoji}</div>
            <div className="stat-label">{stat.label}</div>
            <div className="stat-value">{stat.value}</div>
            <div className="stat-percentage" style={{ color: stat.color }}>
              {stat.percentage.toFixed(1)}%
            </div>
            <div className="stat-bar">
              <motion.div
                className="stat-bar-fill"
                style={{ backgroundColor: stat.color }}
                initial={{ width: 0 }}
                animate={{ width: `${stat.percentage}%` }}
                transition={{ duration: 1, delay: 0.2 }}
              />
            </div>
          </motion.div>
        ))}
      </motion.div>

      <motion.div className="summary-section" variants={itemVariants}>
        <h4>📋 Resumen del Análisis</h4>
        <ul className="summary-list">
          <li>
            <strong>Total de comentarios:</strong> {data.breakdown.total}
          </li>
          <li>
            <strong>Sentimiento general:</strong>{' '}
            <span className={`sentiment-badge sentiment-${data.overall_sentiment}`}>
              {data.overall_sentiment.charAt(0).toUpperCase() + data.overall_sentiment.slice(1)}
            </span>
          </li>
          <li>
            <strong>Puntuación:</strong> {data.sentiment_score}/100
          </li>
          <li>
            <strong>Hora del análisis:</strong> {new Date(data.timestamp).toLocaleTimeString('es-CO')}
          </li>
        </ul>
      </motion.div>
    </motion.div>
  );
}

export default Dashboard;
