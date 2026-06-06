import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Thermometer from './components/Thermometer';
import Dashboard from './components/Dashboard';
import SentimentChart from './components/SentimentChart';
import NewsCards from './components/NewsCards';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshTime, setRefreshTime] = useState(null);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        sources: null,
        limit: 5
      });

      if (response.data.success) {
        setAnalysis(response.data);
        setRefreshTime(new Date());
      }
    } catch (err) {
      console.error('Error fetching analysis:', err);
      setError(err.response?.data?.error || 'Error al obtener análisis. Intenta más tarde.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
    const interval = setInterval(fetchAnalysis, 30 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🌡️ Termómetro de Noticias Colombia</h1>
          <p className="subtitle">Análisis de sentimiento en tiempo real de noticias nacionales</p>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <p>{error}</p>
          </div>
        )}

        <div className="controls">
          <button 
            className="btn-refresh"
            onClick={fetchAnalysis}
            disabled={loading}
          >
            {loading ? 'Analizando...' : '🔄 Analizar Ahora'}
          </button>
          {refreshTime && (
            <p className="refresh-time">
              Última actualización: {refreshTime.toLocaleTimeString('es-CO')}
            </p>
          )}
        </div>

        {analysis ? (
          <>
            <div className="thermometer-section">
              <Thermometer 
                sentiment={analysis.overall_sentiment}
                score={analysis.sentiment_score}
              />
            </div>

            <div className="main-grid">
              <div className="grid-left">
                <Dashboard data={analysis} />
              </div>
              <div className="grid-right">
                <SentimentChart data={analysis.breakdown} />
              </div>
            </div>

            <div className="news-section">
              <NewsCards articles={analysis.articles} />
            </div>
          </>
        ) : loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Cargando análisis de noticias...</p>
          </div>
        ) : (
          <div className="empty-state">
            <p>Haz clic en "Analizar Ahora" para comenzar</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2024 Termómetro de Noticias Colombia | Datos actuales del {new Date().toLocaleDateString('es-CO')}</p>
      </footer>
    </div>
  );
}

export default App;
