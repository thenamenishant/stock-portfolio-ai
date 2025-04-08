# AI-Powered Stock Portfolio App

This project is a full-stack application that integrates AI to assist in analyzing and predicting stock prices using FastAPI (backend) and React.js (frontend).

## 📁 Folder Structure

```
stock-portfolio-ai/
├── ai_backend/
│   ├── main.py
│   ├── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   ├── package.json
├── README.md
```

---

## 🚀 Backend Setup (FastAPI)

### 🧪 Install Requirements
```bash
cd ai_backend
pip install -r requirements.txt
```

### ▶️ Run FastAPI
```bash
uvicorn main:app --reload
```

---

## 🌐 Frontend Setup (React)

### 📦 Install Packages
```bash
cd frontend
npm install
```

### ▶️ Start React App
```bash
npm start
```

---

## 🔗 API Endpoint

- `GET /predict/{ticker}`  
  Predicts the next day's stock price based on historical data.

---

## 🧠 AI Model
- Uses **Linear Regression** from `scikit-learn`
- Fetches historical data using **Yahoo Finance**

---

## 🛠 Tech Stack

- Backend: FastAPI, scikit-learn, yfinance
- Frontend: React.js, Axios
