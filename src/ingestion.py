import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine # NEW: The database connector

# 1. Load the vault (.env file)
load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# 2. Connect to Alpaca
print("Authenticating with Alpaca...")
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# 3. Request the last 5 days of S&P 500 Data
request_params = StockBarsRequest(
    symbol_or_symbols="SPY",
    timeframe=TimeFrame.Day,
    start=datetime.now() - timedelta(days=60)
)

print("Fetching institutional market data...")
raw_data = data_client.get_stock_bars(request_params)
spy_data = raw_data.df

# ---------------------------------------------------------
# PHASE 2: DATABASE STORAGE (The Hedge Fund Route)
# ---------------------------------------------------------
print("Connecting to local SQL Database...")

# 4. Create the SQL Database Engine (This creates a file named 'quant_market_data.db')
engine = create_engine('sqlite:///data/quant_market_data.db')

# 5. Push the Pandas DataFrame directly into a SQL table named 'spy_historical'
# if_exists='replace' means it will update the table with fresh data every time you run it
spy_data.to_sql('spy_historical', engine, if_exists='replace', index=True)

print("\nSUCCESS! Pipeline complete. Data is permanently stored in SQL.")

# 6. Prove it worked by writing a SQL Query in Python
print("\n--- Running Automated SQL Verification Query ---")
verification_query = pd.read_sql("SELECT symbol, timestamp, close, vwap FROM spy_historical LIMIT 3", engine)
print(verification_query)