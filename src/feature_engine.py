import pandas as pd
from sqlalchemy import create_engine

# 1. Connect to your local Quant Database
print("Connecting to the Data Warehouse...")
engine = create_engine('sqlite:///data/quant_market_data.db')

# 2. Extract the raw data using a SQL Query
# We order by timestamp so our mathematical calculations flow in chronological order
print("Extracting raw S&P 500 data...")
query = "SELECT timestamp, close, volume, vwap FROM spy_historical ORDER BY timestamp ASC"
raw_df = pd.read_sql(query, engine)

# ---------------------------------------------------------
# PHASE 3: QUANTITATIVE FEATURE ENGINEERING 
# ---------------------------------------------------------
print("Calculating Quantitative Trading Signals...")

# Feature 1: Daily Return Percentage
# How much did the stock move compared to the day before?
raw_df['daily_return_pct'] = raw_df['close'].pct_change() * 100

# Feature 2: 3-Day Simple Moving Average (SMA)
# Because we only pulled 5 days of data, we will use a short 3-day window for momentum
raw_df['sma_3_day'] = raw_df['close'].rolling(window=3).mean()

# Feature 3: Volume Momentum
# Is today's volume higher than yesterday's? (1 for Yes, 0 for No)
raw_df['volume_surge'] = (raw_df['volume'] > raw_df['volume'].shift(1)).astype(int)

# Clean up the dataset by dropping the initial rows that couldn't calculate a 3-day average
signals_df = raw_df.dropna()

# ---------------------------------------------------------
# LOAD: PUSH BACK TO THE DATABASE
# ---------------------------------------------------------
print("Loading pristine signals into the 'quant_features' SQL table...")
# We save this as a separate table so the Quants have a dedicated place to pull signals
signals_df.to_sql('quant_features', engine, if_exists='replace', index=False)

print("\nSUCCESS! Feature Engineering complete. Here are the signals generated for the Quants:")
# Print a clean view of the new mathematical features
print(signals_df[['timestamp', 'close', 'daily_return_pct', 'sma_3_day', 'volume_surge']])