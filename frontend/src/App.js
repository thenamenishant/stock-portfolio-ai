import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';

function App() {
    const [ticker, setTicker] = useState('');
    const [predictions, setPredictions] = useState([]);
    const [trend, setTrend] = useState('');
    const [news, setNews] = useState([]);
    const [portfolio, setPortfolio] = useState({ expected_return: '', risk_level: '', sector: '', diversification_advice: {} });

    const fetchPredictions = async () => {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker })
        });
        const data = await response.json();
        setPredictions(data.predictions);
        setTrend(data.trend);
        setNews(data.news);
        setPortfolio(data.portfolio);
    };

    const chartData = {
        labels: predictions.map((_, i) => `Day ${i + 1}`),
        datasets: [{
            label: `Stock Predictions for ${ticker.toUpperCase()}`,
            data: predictions,
            borderColor: 'rgba(75,192,192,1)',
            fill: false,
        }]
    };

    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <h1>AI Stock Prediction & Portfolio Insights</h1>
            <input
                type="text"
                placeholder="Enter stock ticker"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
            />
            <button onClick={fetchPredictions}>Predict</button>
            <h2>Trend: {trend}</h2>
            {predictions.length > 0 && <Line data={chartData} />}
            <h2>Latest News</h2>
            <ul>
                {news.map((n, i) => <li key={i}>{n}</li>)}
            </ul>
            <h2>Portfolio Recommendation</h2>
            <p><strong>Expected Return:</strong> {portfolio.expected_return}</p>
            <p><strong>Risk Level:</strong> {portfolio.risk_level}</p>
            <p><strong>Sector:</strong> {portfolio.sector}</p>
            <h3>Diversification Strategy</h3>
            {Object.entries(portfolio.diversification_advice).map(([key, value]) => (
                <p key={key}><strong>{key}:</strong> {value}</p>
            ))}
        </div>
    );
}

export default App;
