# Quantitative Market Data & Feature Engineering Pipeline

## 📌 Business Objective
An automated end-to-end ETL (Extract, Transform, Load) pipeline designed to ingest institutional-grade market data, engineer quantitative trading signals, and load pristine features into a relational data warehouse for algorithmic trading analysis.

## 🏗️ System Architecture
1. **Extraction:** Connects securely to the Alpaca Markets API via Python to pull high-frequency historical tick data (S&P 500).
2. **Transformation (Feature Engineering):** Utilizes Pandas to clean missing data and calculate quantitative momentum signals (Daily Return %, Simple Moving Averages, and Volume Surges).
3. **Load (Data Warehousing):** Pushes the transformed signal data into a structured local SQL database (`SQLite` & `SQLAlchemy`) mimicking enterprise RDBMS environments.
4. **Visualization:** Queries the data warehouse directly to generate professional financial charts using `Matplotlib`.

## 📊 Engineered Features (Data Dictionary)
| Feature Name | Description | Data Type |
| :--- | :--- | :--- |
| `close` | Daily closing price of the asset. | Float |
| `vwap` | Volume-Weighted Average Price. | Float |
| `daily_return_pct`| Percentage change in close price from the previous trading day. | Float |
| `sma_3_day` | 3-Day Simple Moving Average used for short-term momentum tracking. | Float |
| `volume_surge` | Boolean indicator (1 or 0) flagging if daily volume exceeded the previous day. | Integer |

## 🚀 How to Run the Pipeline Locally

**1. Clone the repository and install dependencies:**
```bash
pip install -r requirements.txt