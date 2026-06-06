import React from 'react';
import { motion } from 'framer-motion';
import './SentimentChart.css';

function SentimentChart({ data }) {
  const total = data.positive + data.negative + data.neutral;
  
  const chartData = [
    {
      label: 'Positivos',
      value: data.positive,
      color: '#10b981',
      emoji: '😊'
    },
    {
      label: 'Negativos',
      value: data.negative,
      color: '#ef4444',
      emoji: '😞'
    },
    {
      label: 'Neutrales',
      value: data.neutral,
      color: '#f59e0b',
      emoji: '😐'
    }
  ];

  const getPercentage = (value) => {
    return total > 0 ? ((value / total) * 100).toFixed(1) : 0;
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5 }
    }
  };

  return (
    <motion.div
      className="sentiment-chart-card"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h3 className="chart-title">📈 Distribución de Sentimientos</h3>

      <motion.div className="chart-container" variants={containerVariants}>
        {chartData.map((item, idx) => (
          <motion.div key={idx} className="chart-item" variants={itemVariants}>
            <div className="chart-item-header">
              <span className="chart-emoji">{item.emoji}</span>
              <div className="chart-labels">
                <span className="chart-label">{item.label}</span>
                <span className="chart-count">{item.value}</span>
              </div>
            </div>
            <div className="chart-bar-container">
              <motion.div
                className="chart-bar"
                style={{
                  backgroundColor: item.color,
                  width: '0%'
                }}
                animate={{
                  width: `${getPercentage(item.value)}%`
                }}
                transition={{
                  duration: 1,
                  delay: idx * 0.15,
                  ease: 'easeOut'
                }}
              />
            </div>
            <div className="chart-percentage" style={{ color: item.color }}>
              {getPercentage(item.value)}%
            </div>
          </motion.div>
        ))}
      </motion.div>

      <motion.div className="pie-chart-container" variants={itemVariants}>
        <svg viewBox="0 0 100 100" className="pie-chart">
          <defs>
            <style>{`
              .pie-chart-slice { filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); }
            `}</style>
          </defs>
          
          {chartData.reduce((acc, item, idx) => {
            const prevStartAngle = acc.currentAngle;
            const sliceAngle = (item.value / total) * 360;
            const endAngle = prevStartAngle + sliceAngle;

            const startRad = (prevStartAngle * Math.PI) / 180;
            const endRad = (endAngle * Math.PI) / 180;

            const x1 = 50 + 40 * Math.cos(startRad);
            const y1 = 50 + 40 * Math.sin(startRad);
            const x2 = 50 + 40 * Math.cos(endRad);
            const y2 = 50 + 40 * Math.sin(endRad);

            const largeArc = sliceAngle > 180 ? 1 : 0;

            const path = `M 50 50 L ${x1} ${y1} A 40 40 0 ${largeArc} 1 ${x2} ${y2} Z`;

            acc.paths.push(
              <motion.path
                key={idx}
                d={path}
                fill={item.color}
                className="pie-chart-slice"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 + idx * 0.1, duration: 0.5 }}
              />
            );

            acc.currentAngle = endAngle;
            return acc;
          }, { paths: [], currentAngle: 0 }).paths}

          <circle cx="50" cy="50" r="25" fill="white" />
        </svg>
      </motion.div>

      <motion.div className="summary-stats" variants={itemVariants}>
        <div className="total-comments">
          <span className="label">Total de Comentarios</span>
          <span className="value">{total}</span>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default SentimentChart;
