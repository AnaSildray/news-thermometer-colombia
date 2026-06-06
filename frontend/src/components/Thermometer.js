import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import './Thermometer.css';

function Thermometer({ sentiment, score }) {
  const [displayScore, setDisplayScore] = useState(score);

  useEffect(() => {
    const duration = 1000;
    const startTime = Date.now();
    const startScore = displayScore;
    const difference = score - startScore;

    const updateScore = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      setDisplayScore(Math.round(startScore + difference * progress));

      if (progress < 1) {
        requestAnimationFrame(updateScore);
      }
    };

    requestAnimationFrame(updateScore);
  }, [score]);

  const getColor = () => {
    if (displayScore >= 67) return '#10b981';
    if (displayScore >= 34) return '#f59e0b';
    return '#ef4444';
  };

  const getSentimentLabel = () => {
    if (sentiment === 'positive') return 'Positivo';
    if (sentiment === 'negative') return 'Negativo';
    return 'Neutral';
  };

  const getSentimentDescription = () => {
    if (sentiment === 'positive') return '✨ La situación en el país se ve positiva';
    if (sentiment === 'negative') return '⚠️ La situación en el país se ve negativa';
    return '⚡ La situación en el país es mixta';
  };

  return (
    <div className="thermometer-container">
      <div className="thermometer-card">
        <div className="thermometer-header">
          <h2>Estado del País</h2>
          <span className={`sentiment-badge sentiment-${sentiment}`}>
            {getSentimentLabel()}
          </span>
        </div>

        <div className="thermometer-body">
          <svg className="thermometer-svg" viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="thermGradient" x1="0%" y1="100%" x2="0%" y2="0%">
                <stop offset="0%" stopColor="#ef4444" />
                <stop offset="50%" stopColor="#f59e0b" />
                <stop offset="100%" stopColor="#10b981" />
              </linearGradient>
            </defs>

            <rect x="75" y="20" width="50" height="300" rx="25" fill="#f0f0f0" stroke="#999" strokeWidth="2" />

            <motion.rect
              x="80"
              y={310 - (displayScore * 280) / 100}
              width="40"
              height={(displayScore * 280) / 100}
              rx="20"
              fill={getColor()}
              animate={{ y: 310 - (displayScore * 280) / 100 }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
            />

            <circle cx="100" cy="340" r="25" fill="#f0f0f0" stroke="#999" strokeWidth="2" />
            <motion.circle
              cx="100"
              cy="340"
              r="22"
              fill={getColor()}
              animate={{ r: 20 }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
            />

            {[0, 25, 50, 75, 100].map((mark) => (
              <g key={mark}>
                <line x1="70" y1={310 - (mark * 280) / 100} x2="75" y2={310 - (mark * 280) / 100} stroke="#666" strokeWidth="2" />
                <text x="60" y={315 - (mark * 280) / 100} fontSize="12" fill="#333" textAnchor="end">
                  {mark}
                </text>
              </g>
            ))}

            <text x="135" y="50" fontSize="11" fill="#10b981" fontWeight="bold">
              POSITIVO
            </text>
            <text x="135" y="180" fontSize="11" fill="#f59e0b" fontWeight="bold">
              NEUTRAL
            </text>
            <text x="135" y="310" fontSize="11" fill="#ef4444" fontWeight="bold">
              NEGATIVO
            </text>
          </svg>

          <div className="thermometer-info">
            <motion.div
              className="score-display"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 0.5 }}
            >
              <div className="score-value">{displayScore}%</div>
              <div className="score-label">Índice de Sentimiento</div>
            </motion.div>

            <div className="sentiment-description">
              {getSentimentDescription()}
            </div>
          </div>
        </div>

        <div className="thermometer-legend">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#10b981' }}></div>
            <span>67-100: Situación Positiva</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#f59e0b' }}></div>
            <span>34-66: Situación Neutral</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
            <span>0-33: Situación Negativa</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Thermometer;
