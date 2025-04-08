from fastapi import FastAPI
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")
    return df[['Close']]

def train_model(df):
    df['Days'] = range(len(df))
    X = df[['Days']]
    y = df['Close']
    model = LinearRegression()
    model.fit(X, y)
    return model

def fetch_news_sentiment(ticker):
    api_url = f'https://newsapi.org/v2/everything?q={ticker}&apiKey=YOUR_NEWSAPI_KEY'
    response = requests.get(api_url).json()
    articles = response.get("articles", [])[:5]
    sentiments = [article['title'] for article in articles]
    return sentiments if sentiments else ["No recent news found"]

def recommend_portfolio(ticker):
    df = fetch_stock_data(ticker)
    returns = df['Close'].pct_change().dropna()
    volatility = np.std(returns)
    avg_return = np.mean(returns)
    risk_score = "Low" if volatility < 0.02 else "Medium" if volatility < 0.05 else "High"
    stock = yf.Ticker(ticker)
    sector = stock.info.get("sector", "Unknown")
    diversification_advice = {
        "Low": {
            "Stock Strategy": "Consider adding moderate-risk growth stocks across industries.",
            "Bond Allocation": "Increase allocation to corporate and government bonds.",
            "Real Estate": "Invest in REITs for stable income.",
            "Crypto": "Minimal exposure to crypto, focus on stablecoins.",
            "Regional Diversification": "Invest in stable markets like the US and Europe."
        },
        "Medium": {
            "Stock Strategy": "Diversify into different sectors and regions for risk mitigation.",
            "Bond Allocation": "Hold a balanced mix of bonds and equities.",
            "Real Estate": "Consider a mix of rental properties and REITs.",
            "Crypto": "Allocate a small portion to established cryptocurrencies like BTC and ETH.",
            "Regional Diversification": "Balance investments across US, Europe, and Asia for stability."
        },
        "High": {
            "Stock Strategy": "Reduce exposure to volatile stocks, add defensive stocks.",
            "Bond Allocation": "Increase holdings in bonds to offset risks.",
            "Real Estate": "Focus on commercial properties for stability.",
            "Crypto": "Limit exposure to highly volatile assets.",
            "Regional Diversification": "Avoid high-risk emerging markets, focus on stable regions."
        }
    }
    return {
        "expected_return": f"{avg_return * 100:.2f}% per day",
        "risk_level": risk_score,
        "sector": sector,
        "diversification_advice": diversification_advice[risk_score]
    }

@app.post("/predict")
def predict_stock(data: StockRequest):
    df = fetch_stock_data(data.ticker)
    model = train_model(df)
    future_days = [[len(df) + i] for i in range(1, 6)]
    predictions = model.predict(future_days).tolist()
    trend = "Bullish" if predictions[-1] > df['Close'].iloc[-1] else "Bearish"
    news_sentiment = fetch_news_sentiment(data.ticker)
    portfolio_recommendation = recommend_portfolio(data.ticker)
    return {
        "ticker": data.ticker,
        "predictions": predictions,
        "trend": trend,
        "news": news_sentiment,
        "portfolio": portfolio_recommendation
    }
