import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# 1. Connect to your Quant Database
print("Connecting to the Data Warehouse...")
engine = create_engine('sqlite:///data/quant_market_data.db')

# 2. Extract the engineered signals
print("Pulling Quantitative Features...")
query = "SELECT timestamp, close, sma_3_day FROM quant_features ORDER BY timestamp ASC"
df = pd.read_sql(query, engine)

# Convert timestamp to a cleaner date format for the chart
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

# 3. Build the Financial Chart
print("Generating Portfolio Visualization...")
plt.figure(figsize=(10, 6))

# Plot the actual closing price
plt.plot(df['timestamp'], df['close'], label='S&P 500 Close Price', color='blue', marker='o')

# Plot your engineered feature (The Moving Average)
plt.plot(df['timestamp'], df['sma_3_day'], label='3-Day SMA Signal', color='orange', linestyle='--')

# Format the chart to look professional
plt.title('Quantitative Signals: S&P 500 Price vs. Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price ($)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# Display the dashboard
plt.tight_layout()
plt.show()